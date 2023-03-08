from rest_framework import serializers

from ..models import *
from ..serializers.postserializer import PostSerializer
from ..serializers.commentserializer import CommentSerializer
from ..api_serializers.author_api_serializer import AuthorAPISerializer

# Serializers
post_serializer = PostSerializer()
comment_serializer = CommentSerializer()

# API serializer
author_api_serializer = AuthorAPISerializer()

class CommentAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
    
    def get_post_data(self, comment):
        author_data = author_api_serializer.get_author_data(comment.author)

        comment_data = {
            "type": "comment",
            "id": comment.id,
            "url": comment.url,
            "comment": comment.caption,
            "published": comment.created_at,
            "author": author_data,
            }
        
        return comment_data
    
    def get_post_comments(self, author_id, post_id):
        post = None
        try:
            post = post_serializer.get_author_post(author_id, post_id)
        except ValueError:
            return None
        
        comments = post.comments
        
        result_dict = {}
        result_dict["type"] = "comments"
        result_dict["post"] = post.url
        result_dict["id"] = f"{post.url}/comments"

        comments_list = []

        for comment in comments:
            curr_comment_data = self.get_post_data(comment)
            comments_list.append(curr_comment_data)
 
        result_dict["comments"] = comments_list

        return result_dict
    
    # def add_new_comment(self, author_id, post_id, request_data):
    #     try:
    #         author = author_serializer.get_author_by_id(author_id)
    #         post = post_serializer.get_author_post(author_id, post_id)