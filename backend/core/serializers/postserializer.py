# Built-in libraries
import base64
from uuid import uuid4

# Third-party libraries
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from varname import nameof        

# Local libraries
from .. models import *
from ..serializers.authorserializer import AuthorSerializer
from django.core.files.base import ContentFile
        

author_serializer = AuthorSerializer()

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {'image': {'required': False, 'allow_null': True}}

    def create_post(self, author_id, post_id=None, title=None, content=None, image=None, is_private=False):
        try:
            author = author_serializer.get_author_by_id(author_id)
        except ValueError:
            print("Author does not exist")
            return None
            # raise ValueError("Author does not exist")

        defaults = {
            nameof(Post.author): author,
            nameof(Post.title): title,
            nameof(Post.content): content,
            nameof(Post.image): image,
            nameof(Post.is_private): is_private
        }

        if post_id:
            defaults["id"] = post_id

        if image is not None:
            image_name = uuid4()
            extension = "png"

            image_filename = f"{image_name}.{extension}"

            image_file = ContentFile(base64.b64decode(image), name=image_filename)
            defaults["image"] = image_file

        post = Post.objects.create(**defaults)

        return post.id

    def get_author_post(self, author_id, post_id):
        author = None
        post = None
        try:
            author = author_serializer.get_author_by_id(author_id)
        except ValidationError:
            raise ValidationError("Author does not exist.")
        
        try:
            post = Post.objects.get(pk=post_id, author=author)
        except Post.DoesNotExist:
            raise ValidationError("Post does not exist.")
        
        return post
    
    def update_post(self, author_id, post_id, title=None, content=None, image=None, is_private=False):
        try:
            post = self.get_author_post(author_id, post_id)
        except ValidationError:
            return None
        
        defaults = {
            nameof(Post.title): title,
            nameof(Post.content): content,
            nameof(Post.image): image,
            nameof(Post.is_private): is_private
        }

        updated_post = Post.objects.update(**defaults)

        return updated_post

    def delete_post(self, author_id, post_id):
        try:
            post = self.get_author_post(author_id, post_id)
        except ValidationError:
            return None

        post.delete()

        return post

