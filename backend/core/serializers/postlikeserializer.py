# Local libraries
from ..models import *

# Third-party libraries
from rest_framework import serializers
from varname import nameof
from .authorserializer import AuthorSerializer

class PostLikeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(required=False, max_length=10, default="like", read_only=True)
    summary = serializers.CharField(required=False)
    author = AuthorSerializer(required=True)
    object = serializers.URLField(required=True)

    class Meta:
        model = PostLike
        fields = ["type", "summary", "author", "object"]

    def create_like(self, author_id, post_id):

        print(author_id)
        try:
            like_author_obj = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            raise ValueError("Like Author does not exist")
        
        print("Like author id: ", like_author_obj.id)
        
        try:
            post_obj = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise ValueError("Post does not exist")
        
        print("Post id: ", post_obj.id)

        defaults = {
            nameof(PostLike.author): like_author_obj,
            nameof(PostLike.post): post_obj
        }

        like_obj = PostLike.objects.create(**defaults)

        return like_obj.id
    
    def get_like_by_id(self, author_id, post_id):
        # try:
        #     author = Author.objects.get(pk=author_id)
        # except Author.DoesNotExist:
        #     raise ValueError("Author does not exist.")
        
        # try:
        #     post = Post.objects.get(pk=post_id, author=author)
        # except Post.DoesNotExist:
        #     raise ValueError("Post does not exist.")
        
        try:
            like = PostLike.objects.get()
        except PostLike.DoesNotExist:
            raise ValueError("Like does not exist.")
        
        return like