# Third-party libraries
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Local libraries
from .. import utils
from ..models import *
from ..serializers.authorserializer import AuthorSerializer
from ..serializers.postserializer import PostSerializer, PostListSerializer
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
        keys = list(request_data.keys())
        if "image" not in keys and "content" not in keys:
            print("Require either content or image for the post")
            return None

        title = request_data["title"] if "title" in keys else None
        content = request_data["content"] if "content" in keys else None
        image = request_data["image"] if "image" in keys else None
        is_private = request_data["is_private"] if "is_private" in keys else False

        new_post_id = post_serializer.create_post(post_id=post_id, author_id=author_id, title=title, content=content, image=image, is_private=is_private)

        return self.get_single_post(author_id, new_post_id)
    
    def get_single_post(self, author_id, post_id):
        # Get post by author_id and post_id
        try:
            post = post_serializer.get_author_post(author_id, post_id)
        except ValueError:
            return None

        post_data = self.get_post_data(post)
        return post_data

    def get_all_author_posts(self, author_id, page=None, size=None):
        author = None
        try:
            author = author_serializer.get_author_by_id(author_id)
        except ValidationError:
            return None
        
        posts = author.post.all()

        # serializer = PostListSerializer(posts, many=True)

        result_dict = {}
        result_dict["type"] = "posts"

        posts_list = []

        for post in posts:
            curr_post_data = self.get_post_data(post)
            posts_list.append(curr_post_data)

        if page and size:
            paginated_posts = utils.paginate_list(posts_list, page, size)
            
            result_dict["page"] = page
            result_dict["size"] = size
            result_dict["items"] = paginated_posts
        else:
            result_dict["items"] = posts_list

        return result_dict

    # TODO: needs update
    def update_author_post(self, author_id, post_id, request_data):
        defaults = {}
        for key in request_data:
            if key == "title":
                defaults["title"] = request_data[key]
            elif key == "content":
                defaults["content"] = request_data[key]
            elif key == "visibility":
                defaults["is_private"] = request_data[key]

        updated_post = post_serializer.update_post(author_id=author_id, post_id=post_id, defaults=defaults)

        return self.get_post_data(updated_post)

    def delete_author_post(self, author_id, post_id):
        deleted_post = post_serializer.delete_post(author_id, post_id)

        return deleted_post
