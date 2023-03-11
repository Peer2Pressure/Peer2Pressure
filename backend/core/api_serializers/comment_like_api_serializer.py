from rest_framework import serializers

from ..models import *
from ..serializers.postserializer import PostSerializer
from ..serializers.commentserializer import CommentSerializer
from .author_api_serializer import AuthorAPISerializer

# Serializers
comment_serializer = CommentSerializer()
post_serializer = PostSerializer()

# API serializer
author_api_serializer = AuthorAPISerializer()

class CommentLikeAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"
    
    def get_comment_like_data(self, post_like):
        author_data = author_api_serializer.get_author_data(post_like.author)

        post_like_data = {
            "type": "like",
            "summary": f"{author_data['displayName']} likes your post",
            "author": author_data,
            "object": post_like.post.url
            }
        
        return post_like_data

    def get_all_comment_likes(self, author_id, post_id, comment_id):
        try:
            comment = comment_serializer.get_comment_by_id(author_id, post_id, comment_id)
        except ValueError:
            return None
        
        comment_likes = comment.comment_like.all()

        result_dict = {}
        result_dict["type"] = "comment_likes"

        comment_likes_list = []

        for like in comment_likes:
            curr_comment_like_data = self.get_comment_like_data(like)
            comment_likes_list.append(curr_comment_like_data)

        result_dict["items"] = comment_likes_list

        return result_dict
