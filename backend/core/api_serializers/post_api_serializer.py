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
            "id": post.id,
            "url": post.url,
            "title": post.title,
            "content": post.content,
            "visibility": "private"if post.is_private else "public", 
            "image": f"{author_data['host']}{post.image.url}" if post.image else None,
            "author": author_data,
            }
        
        return post_data

    def get_all_author_posts(self, author_id):
        author = None
        try:
            author = author_serializer.get_author_by_id(author_id)
        except ValueError:
            return None
        
        posts = Post.objects.filter(author=author)

        result_dict = {}
        result_dict["type"] = "posts"

        posts_list = []

        for post in posts:
            curr_post_data = self.get_post_data(post)
            posts_list.append(curr_post_data)

        result_dict["items"] = posts_list

        return result_dict
    
    def get_a_post(self, authorid, postid):
        result_dict = {}

        result_dict["type"] = "post"
        # TODO: Need to add title to POST Model
        result_dict["title"] = ""

        # TODO: Need to handle the case if post or author doesn't exist
        post_obj = post_serializer.get_post(authorid, postid)
        author = author_serializer.get_author_by_id(authorid)

        result_dict["id"] = str(author.host) + "/authors/" + str(authorid) + "/posts/" + str(postid)

        # TODO: Need to find source and origin
        result_dict["origin"] = ""
        result_dict["source"] = ""

        # TODO: Need to add Description for POST Model
        result_dict["description"] = ""

        # TODO: Need to support multiple formats
        result_dict["contentType"] = "text/plain"

        result_dict["content"] = post_obj.caption

        result_dict["author"] = author_api_serializer.get_single_author(authorid)

        # TODO: Need to add way to organize the post to categories
        result_dict["categories"] = []

        # TODO: Need to get the serailzier with get_count for number of comments for post
        result_dict["count"] = 0

        # TODO: Need to get the first page of comments
        result_dict["comments"] = ""

        # TODO: Need to convert the created_at to ISO 8601 TIMESTAMP
        result_dict["published"] = post_obj.created_at

        # TODO: Need to set the visibility to actual visibility
        result_dict["visibility"] = "PUBLIC"

        # TODO: Need to find what unlisted mean
        result_dict["unlisted"] = False

        return result_dict