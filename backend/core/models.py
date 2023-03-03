import uuid
from abc import abstractclassmethod
from datetime import datetime
from varname import nameof
from typing import List

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

MAX_CHARFIELD_LENGTH = 300
HOST = "http://127.0.0.1:8000"

class AbstractModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    @abstractclassmethod
    def get_default_fields(cls) -> List[str]:
        """
            Return the list of default fields when doing a `select *`.
            These are only specific for the model, and irrelevant when doing `select **` (return all fields).
        """
        raise NotImplementedError()

    def __repr__(self):
        return str(self)

class Author(AbstractModel):
    # type = models.CharField(max_length=10, default="author")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="author_profile")
    host = models.URLField(default=HOST)
    username = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=True)
    first_name = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=True)
    last_name = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=True)
    url = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=True)
    email = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=True)
    password = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=True)
    avatar = models.ImageField(upload_to="profile_images", null=True, blank=True, default="/profile_images/default-user.jpeg")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["username", "email", "password"], name="Unique user properties")]

    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.username), nameof(cls.first_name), nameof(cls.last_name), nameof(cls.host)]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.url:
            # Generate a URL based on the object's ID
            self.url = f"{HOST}/{self.id}"
        super().save(*args, **kwargs)

class Relation(AbstractModel):
    to_author = models.ForeignKey(Author, related_name='follower', on_delete=models.CASCADE)
    from_author = models.ForeignKey(Author, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    from_author_request = models.BooleanField(default=False)
    to_author_request = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["from_author", "to_author"], name="There can only be this relation between two authors")]

    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.from_author), nameof(cls.to_author), nameof(cls.from_author_request), nameof(cls.to_author_request)]
    
    def __str__(self):
        return self.from_author.username + " : " + self.to_author.username


class Post(AbstractModel):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    url = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=True)
    title = models.CharField(max_length=MAX_CHARFIELD_LENGTH, blank=True, default="")
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    content = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now)
    is_private = models.BooleanField(default=False)

    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.author)]

    def __str__(self):
        return self.url
    
    def save(self, *args, **kwargs):
        if not self.url:
            # Generate a URL based on the object's ID
            self.url = f"{self.author.url}/{self.id}"
        super().save(*args, **kwargs)

class Like(AbstractModel):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["author", "post"], name="A user can only like post onces")]

    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.author), nameof(cls.post)]
    
    def __str__(self):
        return self.author

class Comment(AbstractModel):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(default="")
    created_at = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.author), nameof(cls.post), nameof(cls.comment)]
    
    def __str__(self):
        return self.author
