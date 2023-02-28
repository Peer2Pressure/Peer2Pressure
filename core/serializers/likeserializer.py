# Local libraries
from .. models import *

# Third-party libraries
from rest_framework import serializers
from varname import nameof        

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"

    def create_like(self, like_author, post):

        try:
            like_author_obj = Author.objects.get(id=like_author)
        except Author.DoesNotExist:
            raise ValueError("Like Author does not exist")
        
        try:
            post_obj = Post.objects.get(id=post)
        except Post.DoesNotExist:
            raise ValueError("Post does not exist")
        
        defaults = {
            nameof(Like.like_author): like_author_obj,
            nameof(Like.post): post_obj
        }

        like_obj = Like.objects.create(**defaults)

        return like_obj.id
