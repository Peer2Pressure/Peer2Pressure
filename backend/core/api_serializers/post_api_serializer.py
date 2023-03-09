# Third-party libraries
from rest_framework import serializers

# Local libraries
from ..models import *
from ..serializers.authorserializer import AuthorSerializer
from ..serializers.relationserializer import RelationSerializer
from ..serializers.postserializer import PostSerializer
from ..serializers.commentserializer import CommentSerializer
from ..api_serializers.author_api_serializer import AuthorAPISerializer

# Serializers
author_serializer = AuthorSerializer()
post_serializer = PostSerializer()

# API Serializer
author_api_serializer = AuthorAPISerializer()


class PostAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def get_post_data(self, post):
        author_data = author_api_serializer.get_author_data(post.author)

        post_data = {
            "type": "post",
            "id": post.url,
            "title": post.title,
            "content": post.content,
            "visibility": "private"if post.is_private else "public", 
            "image": f"{author_data['host']}{post.image.url}" if post.image else None,
            "author": author_data,
            }
        
        return post_data

    def add_new_post(self, author_id, request_data):
        keys = list(request_data.keys())
        if "image" not in keys and "content" not in keys:
            print("Require either content or image for the post")
            return None

        title = request_data["title"] if "title" in keys else None
        content = request_data["content"] if "content" in keys else None
        image = request_data["image"] if "image" in keys else None
        is_private = request_data["is_private"] if "is_private" in keys else False

        post_id = post_serializer.create_post(author_id=author_id, title=title, content=content, image=image, is_private=is_private)

        return self.get_single_post(author_id, post_id)
    
    def get_single_post(self, author_id, post_id):
        post_data = {}
        try:
            post = post_serializer.get_author_post(author_id, post_id)
            post_data = self.get_post_data(post)
        except ValueError:
            return None
        
        return post_data

    def get_all_author_posts(self, author_id):
        author = None
        try:
            author = author_serializer.get_author_by_id(author_id)
        except ValueError:
            return None
        
        posts = author.post.all()

        result_dict = {}
        result_dict["type"] = "posts"

        posts_list = []

        for post in posts:
            curr_post_data = self.get_post_data(post)
            posts_list.append(curr_post_data)

        result_dict["items"] = posts_list

        return result_dict
