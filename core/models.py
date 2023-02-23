from abc import abstractclassmethod
from django.db import models
from typing import List
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from varname import nameof

MAX_CharField_Lenght = 150

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

class User(AbstractModel):
    username = models.CharField(max_length=MAX_CharField_Lenght, blank=True)
    first_name = models.CharField(max_length=MAX_CharField_Lenght, blank=True)
    last_name = models.CharField(max_length=MAX_CharField_Lenght, blank=True)
    email = models.CharField(max_length=MAX_CharField_Lenght, blank=True)
    password = models.CharField(max_length=MAX_CharField_Lenght, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["username", "first_name", "last_name", "email", "password"], name="Unique user properties")]

    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.username), nameof(cls.first_name), nameof(cls.last_name)]

    def __str__(self):
        return self.username

class Post(AbstractModel):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # username = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    is_private = models.BooleanField(default=False)

    @classmethod
    def get_default_fields(cls) -> List[str]:
        return [nameof(cls.author)]

    def __str__(self):
        return self.caption
