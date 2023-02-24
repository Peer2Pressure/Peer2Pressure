from abc import abstractclassmethod
from django.db import models
from typing import List
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from varname import nameof
from django.utils import timezone

MAX_CharField_Length = 150
Local_host = "http://127.0.0.1:5454"

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
    host = models.URLField(default=Local_host)
    username = models.CharField(max_length=MAX_CharField_Length, blank=True)
    first_name = models.CharField(max_length=MAX_CharField_Length, blank=True)
    last_name = models.CharField(max_length=MAX_CharField_Length, blank=True)
    email = models.CharField(max_length=MAX_CharField_Length, blank=True)
    password = models.CharField(max_length=MAX_CharField_Length, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["username", "email", "password"], name="Unique user properties")]

    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.username), nameof(cls.first_name), nameof(cls.last_name), nameof(cls.host)]

    def __str__(self):
        return self.username

class Relations(AbstractModel):
    from_author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='relations_from_author')
    to_author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='relations_to_author')
    created_at = models.DateTimeField(default=timezone.now)
    from_author_request = models.BooleanField(default=False)
    to_author_request = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["from_author", "to_author"], name="There can only be this relation between two authors")]

    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.from_author), nameof(cls.to_author), nameof(cls.from_author_request), nameof(cls.to_author_request)]
    
    def __str__(self) -> str:
        return self.from_author

class Post(AbstractModel):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # username = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images', blank=True)
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_private = models.BooleanField(default=False)

    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.author)]

    def __str__(self):
        return self.caption

class Like(AbstractModel):
    like_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["like_author", "post"], name="A user can only like post onces")]

    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.like_author), nameof(cls.post)]
    
    def __str__(self):
        return self.like_author

class Comment(AbstractModel):
    comment_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.comment_author), nameof(cls.post), nameof(cls.comment)]
    
    def __str__(self):
        return self.comment_author