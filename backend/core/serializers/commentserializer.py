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
    type = serializers.CharField(required=False, max_length=10, default="comment", read_only=True)
    author = AuthorSerializer(required=True)
    comment = serializers.CharField(required=True)
    contentType = serializers.CharField(source="content_type", required=True)
    object = serializers.URLField(required=True)

    class Meta:
        model = Comment
        fields = ["type", "author", "comment", "contentType", "object"]

    def get_comment_post(self, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise ValueError("Comment does not exist.")
        
        return comment.post

    # TODO: Need to modify this to include all the fields in the comment model    
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

    def get_comment_by_id(self, comment_id):
        
        try:
            # print("Comment id: ", comment_id)
            comment = Comment.objects.get(pk=comment_id)
            # print("Comment: ", comment)
        except Comment.DoesNotExist:
            raise ValueError("Comment does not exist")
        
        return comment  