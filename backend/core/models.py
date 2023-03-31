import os 
from uuid import uuid4
from abc import abstractclassmethod
from varname import nameof
from typing import List

# Third-party libraries
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Local Libraries
from .config import *

MAX_CHARFIELD_LENGTH = 512

class AbstractModel(models.Model):
    class Meta:
        abstract = True

    m_id = models.UUIDField(primary_key=True, default=uuid4)
    
    @abstractclassmethod
    def get_default_fields(cls) -> List[str]:
        """
            Return the list of default fields when doing a `select *`.
            These are only specific for the model, and irrelevant when doing `select **` (return all fields).
        """
        raise NotImplementedError()

    def __repr__(self):
        return str(self)


class Node(AbstractModel):
    api_endpoint = models.CharField(max_length=MAX_CHARFIELD_LENGTH, default="")
    token = models.CharField(max_length=MAX_CHARFIELD_LENGTH, default="")

    def __str__(self):
        return str(self.api_endpoint)
    

class Author(AbstractModel):
    id = models.URLField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="author_profile", default=None, null=True)
    host = models.URLField(default=BASE_HOST)
    username = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=True)
    name = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=True)
    url = models.URLField()
    email = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=True)
    password = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=True)
    avatar = models.URLField(default="", blank=True, null=True)
    github = models.URLField(default="", blank=True, null=True)
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=["id"], name="Unique user properties")]

    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.username), nameof(cls.name), nameof(cls.host)]

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.url:
            # Generate a URL based on the object's ID
            self.id = f"{BASE_HOST}/authors/{self.m_id}"
            self.url = f"{BASE_HOST}/authors/{self.m_id}"
        super().save(*args, **kwargs)


class Follower(AbstractModel):
    to_author = models.ForeignKey(Author, related_name='follower', on_delete=models.CASCADE)
    from_author = models.ForeignKey(Author, related_name='following', on_delete=models.CASCADE)
    summary = models.CharField(max_length=MAX_CHARFIELD_LENGTH, default="")
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["from_author", "to_author"], name="There can only be this relation between two authors")]

    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.from_author), nameof(cls.to_author), nameof(cls.from_author_request), nameof(cls.to_author_request)]
    
    def __str__(self):
        return str(self.from_author.name)+" -> "+str(self.to_author.name)


class Post(AbstractModel):
    id = models.URLField(default="")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="post")
    url = models.URLField(default="")
    title = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=True, default="")
    image_url = models.URLField(default="")
    content = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now)
    visibility = models.CharField(max_length=MAX_CHARFIELD_LENGTH, default="PUBLIC")
    source = models.URLField(blank=True)
    origin = models.URLField(blank=True)
    description = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=True, default="")
    content_type = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=False, null=False)
    comments = models.URLField(default="")
    # categories = models.ArrayField(models.CharField)
    unlisted = models.BooleanField(default=False)

    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.author)]

    def __str__(self):
        return self.author.name + " post:" +str(self.id)
    
    def save(self, *args, **kwargs):
        if not self.url:
            # Generate a URL based on the object's ID
            self.id = f"{self.author.url}/posts/{self.m_id}"
            self.url = f"{self.author.url}/posts/{self.m_id}"
            self.comments = f"{self.id}/comments"
        super().save(*args, **kwargs)


class Comment(AbstractModel):
    type = models.CharField(max_length=MAX_CHARFIELD_LENGTH, default="comment")
    id = models.URLField(default="")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    comment = models.TextField(default="")
    url = models.URLField(default="")
    content_type = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=False, null=False, default="text/plain")
    created_at = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    object = models.URLField(default="")

    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.author), nameof(cls.post), nameof(cls.comment)]

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        # TODO: Need to update this id and url to be self.author.url instead of self.post.url
        if not self.url:
            # Generate a URL based on the object's ID
            self.id = f"{self.post.url}/comments/{self.m_id}"
            self.url = f"{self.post.url}/comments/{self.m_id}"
        super().save(*args, **kwargs)


class PostLike(AbstractModel):
    type = models.CharField(max_length=MAX_CHARFIELD_LENGTH, default="like")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")
    created_at = models.DateTimeField(default=timezone.now)
    summary = models.CharField(max_length=MAX_CHARFIELD_LENGTH, default="")
    object = models.URLField(default="")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["author", "post"], name="A user can only like post onces")]


    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.author), nameof(cls.post)]


class CommentLike(AbstractModel):
    type = models.CharField(max_length=MAX_CHARFIELD_LENGTH, default="like")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comment_like")
    created_at = models.DateTimeField(default=timezone.now)
    summary = models.CharField(max_length=MAX_CHARFIELD_LENGTH, default="")
    object = models.URLField(default="")

    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.author), nameof(cls.comment)]


class Inbox(AbstractModel):
    type = models.CharField(max_length=MAX_CHARFIELD_LENGTH, default="post")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, related_name="inbox")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(default=timezone.now)
    
    # post = 1
    # comment =1
    # post_like = 2
    # comment_like = 3