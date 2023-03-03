# Local libraries
from .. models import *

# Third-party libraries
from rest_framework import serializers
from varname import nameof        

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
    
    def create_comment(self, author_id, post_id, comment):

        try:
            comment_author_obj = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            raise ValueError("Comment Author does not exist")
        
        try:
            post_obj = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise ValueError("Post does not exist")
        
        defaults = {
            nameof(Comment.comment_author): comment_author_obj,
            nameof(Comment.post): post_obj,
            nameof(comment): comment
        }

        comment_obj, comment_created = Comment.objects.create(defaults=defaults)

        return comment_obj.id, comment_created        
