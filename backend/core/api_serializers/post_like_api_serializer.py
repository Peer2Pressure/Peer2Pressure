from rest_framework import serializers

from ..models import *
from ..serializers.postserializer import PostSerializer
from .author_api_serializer import AuthorAPISerializer

# Serializers
post_serializer = PostSerializer()

# API serializer
author_api_serializer = AuthorAPISerializer()

class PostLikeAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"
    
    def get_post_like_data(self, post_like):
        author_data = author_api_serializer.get_author_data(post_like.author)

        post_like_data = {
            "type": "like",
            "summary": f"{author_data['displayName']} likes your post",
            "author": author_data,
            "object": post_like.post.url
            }
        
        return post_like_data

    def get_all_post_likes(self, author_id, post_id):
        try:
            post = post_serializer.get_author_post(author_id, post_id)
        except ValueError:
            return None
        
        post_likes = post.post_like.all()

        result_dict = {}
        result_dict["type"] = "likes"

        post_likes_list = []

        for like in post_likes:
            curr_post_like_data = self.get_post_like_data(like)
            post_likes_list.append(curr_post_like_data)

        result_dict["items"] = post_likes_list

        return result_dict

    def get_all_post_likes_by_author(self, author_id):
        try:
            author = author_api_serializer.get_single_author(author_id)
        except ValueError:
            return None
        
        post_likes = PostLike.objects.filter(author=author_id)

        result_dict = {}
        result_dict["type"] = "liked"

        post_likes_list = []

        for like in post_likes:
            curr_post_like_data = self.get_post_like_data(like)
            post_likes_list.append(curr_post_like_data)

        result_dict["items"] = post_likes_list

        return result_dict