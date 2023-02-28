# Local libraries
from .. models import *

# Third-party libraries
from rest_framework import serializers
from varname import nameof        

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
    
    def create_comment(self, comment_author, post, comment):

        try:
            comment_author_obj = Author.objects.get(id=comment_author)
        except Author.DoesNotExist:
            raise ValueError("Comment Author does not exist")
        
        try:
            post_obj = Post.objects.get(id = post)
        except Post.DoesNotExist:
            raise ValueError("Post does not exist")
        
        defaults = {
            nameof(Comment.comment_author): comment_author_obj,
            nameof(Comment.post): post_obj,
            nameof(comment): comment
        }

        comment_obj, comment_created = Comment.objects.create(defaults=defaults)

        return comment_obj.id, comment_created        