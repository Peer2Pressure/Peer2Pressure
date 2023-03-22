# Local libraries
from .. models import *
from ..serializers.authorserializer import AuthorSerializer
from ..serializers.postserializer import PostSerializer

# Third-party libraries
from rest_framework import serializers
from varname import nameof        

author_serializer = AuthorSerializer()
post_serializer = PostSerializer()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
    
    def create_comment(self, author_id, post_id, comment):

        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            raise ValueError("Author does not exist")
        
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise ValueError("Post does not exist")
        
        defaults = {
            nameof(Comment.author): author,
            nameof(Comment.post): post,
            nameof(Comment.comment): comment
        }

        comment_obj = Comment.objects.create(**defaults)

        return comment_obj.id

    def get_comment_by_id(self, author_id, post_id, comment_id):
        try:
            author = author_serializer.get_author_by_id(author_id)
        except ValueError:
            raise ValueError("Author does not exist.")
        
        try:
            post = Post.objects.get(pk=post_id, author=author)
        except Post.DoesNotExist:
            raise ValueError("Post does not exist.")
        
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise ValueError("Comment does not exist")
        
        return comment  
