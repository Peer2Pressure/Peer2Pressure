# Third-party libraries
from django.core.paginator import Paginator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


# Local libraries
from .. import utils
from ..models import *
from ..serializers.authorserializer import AuthorSerializer
from ..serializers.postserializer import PostSerializer, AllPostSerializer
from ..api_serializers.author_api_serializer import AuthorAPISerializer
from ..api_serializers.comment_api_serializer import CommentAPISerializer

# Serializers
author_serializer = AuthorSerializer()
post_serializer = PostSerializer()

# API Serializer
author_api_serializer = AuthorAPISerializer()
comment_api_serializer = CommentAPISerializer()

class PostAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def get_post_data(self, post):
        author_data = author_api_serializer.get_author_data(post.author)
        comments_data = comment_api_serializer.get_post_comments(post.author.id, post.id, page=1, size=5)

        post_data = {
            "type": "post",
            "title": post.title,
            "id": post.url,
            "source": "",
            "origin": "",
            "description": "",
            "contentType": "",
            "content": post.content,
            "author": author_data,
            "categories": [],
            # comments count
            "count": "",
            "comments": f"{post.url}/comments",           
            "commentsSrc": comments_data,
            "published": post.created_at,
            "visibility": "FRIENDS"if post.is_private else "PUBLIC", 
            # "image": f"{author_data['host']}{post.image.url}" if post.image else None,
            }
        
        return post_data


    def add_new_post(self, author_id, request_data, post_id=None):
        print("\n\n ADDING", request_data, type(request_data), "\n\n")

        if not author_serializer.author_exists(author_id):
            return {"msg": "Author does not exist."}, 404

        author = author_serializer.get_author_by_id(author_id)    
        
        valid_content_types = ["text/markdown", "text/plain", "application/base64"]
        valid_image_content_types = ["image/png;base64", "image/jpeg;base64"]

        serializer = PostSerializer(data=request_data)
        errors = {}
        if serializer.is_valid():
            validated_post_data = serializer.validated_data
            print("\n\n ADDING", validated_post_data, type(validated_post_data), "\n\n")

            if validated_post_data["content_type"] not in valid_content_types+valid_image_content_types :
                errors["contentType"] = f"Inavlid contentType. Valid values: {valid_content_types+valid_image_content_types}"

            if validated_post_data["content"] == "":
                if validated_post_data["content_type"] not in valid_image_content_types:
                    errors["content"] = f"Cannot post empty content for contentTypes: {valid_content_types}"
                if validated_post_data["content_type"] in valid_image_content_types:
                    errors["content"] = f"No image data found."
            
            if len(errors) > 0:
                return errors, 400
            
            validated_post_data["author"] = author
            if post_id:
                validated_post_data["m_id"] = post_id
            post = serializer.create(validated_post_data)
            print("ADD\n\n", validated_post_data)
            post.save()
            print("SAVEEDDD\n\n")
            return PostSerializer(post).data, 201

        else:
            return serializer.errors, 400
    
    def get_single_post(self, author_id, post_id):
        # Get post by author_id and post_id
        try:
            post = post_serializer.get_author_post(author_id, post_id)
        except ValidationError:
            return None

        serializer = PostSerializer(post)

        return serializer.data

    def get_all_author_posts(self, author_id, page=None, size=None):
        try:
            author = author_serializer.get_author_by_id(author_id)
        except ValidationError as e:
            return {"msg": str(e)}, 404
        
        posts = author.post.all()

        if page and size:
            paginator = Paginator(posts, size)
            if page > paginator.num_pages:
                return {}, 404
            posts = paginator.get_page(page)

        filtered_posts = [post for post in posts if post.visibility == "PUBLIC" and post.unlisted == False]

        post_serializer = PostSerializer(filtered_posts, many=True)


        serializer = AllPostSerializer(data={
                        'type': 'posts',
                        'page': page,
                        'size': size,
                        'items': post_serializer.data
                    })

        if serializer.is_valid():
            return serializer.data, 200
        else:
            return serializer.errors, 400

    def update_author_post(self, author_id, post_id, request_data):
        # print(pos)
        try:
            post = post_serializer.get_author_post(author_id, post_id)
        except ValidationError as e:
            return {"msg": str(e)}, 404
        
        print("\n\nUPDATING ", request_data, type(request_data), "\n\n")

        valid_content_types = ["text/markdown", "text/plain", "application/base64"]
        valid_image_content_types = ["image/png;base64", "image/jpeg;base64"]

        serializer = PostSerializer(post, request_data)

        errors = {}

        if serializer.is_valid():
            validated_post_data = serializer.validated_data
            print("validated", validated_post_data)
            
            if validated_post_data["content_type"] not in valid_content_types+valid_image_content_types :
                errors["content_type"] = f"Inavlid contentType. Valid values: {valid_content_types+valid_image_content_types}"
            
            if validated_post_data["content"] == "":
                if validated_post_data["content_type"] not in valid_image_content_types:
                    errors["content"] = f"Cannot post empty content for contentTypes: {valid_content_types}"
                if validated_post_data["content_type"] in valid_image_content_types:
                    errors["content"] = f"No image data found."


            if len(errors) > 0:
                return errors, 400

            validated_post_data.pop("author")
            print("UPDATE\n\n", validated_post_data)
            serializer.save()
            print("SAving 1112 update \n\n",)
            post = post_serializer.get_author_post(author_id, post_id)
            return PostSerializer(post).data, 200
        else:
            return serializer.errors, 400

    def delete_author_post(self, author_id, post_id):
        deleted_post = post_serializer.delete_post(author_id, post_id)

        return deleted_post