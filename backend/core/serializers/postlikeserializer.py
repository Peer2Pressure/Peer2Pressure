# Local libraries
from ..models import *

# Third-party libraries
from rest_framework import serializers
from varname import nameof        

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"

    def create_like(self, author_id, post_id):

        try:
            like_author_obj = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            raise ValueError("Like Author does not exist")
        
        try:
            post_obj = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise ValueError("Post does not exist")
        
        defaults = {
            nameof(PostLike.author): like_author_obj,
            nameof(PostLike.post): post_obj
        }

        like_obj = PostLike.objects.create(**defaults)

        return like_obj.id
    
    
