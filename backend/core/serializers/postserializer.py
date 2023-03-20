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
    type = serializers.CharField(required=False, max_length=10, default="post", read_only=True)
    title = serializers.CharField(required=False, max_length=300)
    id = serializers.URLField(required=False, source="url")
    source = serializers.URLField(required=False, allow_blank=True)
    origin = serializers.URLField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    contentType = serializers.CharField(source="content_type", required=False)
    content = serializers.CharField(required=False)
    # image = serializers.ImageField(required=False, default="")
    author = AuthorSerializer(required=False)
    # categories = serializers.ListField(child=serializers.CharField(max_length=100), required=False)
    comments = serializers.URLField(required=False, allow_blank=True)
    # commentSrc = 
    published = serializers.DateTimeField(source="created_at", required=False)
    visibility = serializers.CharField(max_length=10, default="PUBLIC", required=False)
    unlisted = serializers.BooleanField(default=False, required=False)
    class Meta:
        model = Post
        fields = ["type", "title", "id", "source", "origin", "description", "contentType",
                "content", "author", "comments", "published", "visibility", "unlisted" ]
        # fields = "__all__"
        extra_kwargs = {'image': {'required': False, 'allow_null': True}}

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


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
    
    def update_post(self, author_id, post_id, defaults=None, title=None, content=None, image=None, is_private=False):
        try:
            post = self.get_author_post(author_id, post_id)
        except ValidationError:
            return None
        
        if not defaults:
            defaults = {
                nameof(Post.title): title,
                nameof(Post.content): content,
                nameof(Post.image): image,
                nameof(Post.is_private): is_private
            }

        updated_post = Post.objects.filter(pk=post_id).update(**defaults)

        updated_post = self.get_author_post(author_id, post_id)

        return updated_post

    def delete_post(self, author_id, post_id):
        try:
            post = self.get_author_post(author_id, post_id)
        except ValidationError:
            return None

        post.delete()

        return post

class AllPostSerializer(serializers.Serializer):
    type = serializers.CharField(default="posts" , max_length=10, read_only=True, required=False)
    page = serializers.IntegerField(allow_null=True, required=False)
    size = serializers.IntegerField(allow_null=True, required=False)
    items = PostSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['page'] is None:
            data.pop('page')
        if data['size'] is None:
            data.pop('size')
        return data