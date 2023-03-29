import requests
import json
from urllib.parse import urlparse
import uuid
import pprint

# Third-party libraries
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse

# Local libraries
from .. import utils
from ..models import *
from ..serializers.authorserializer import AuthorSerializer
from ..serializers.postserializer import PostSerializer
from ..serializers.followerserializer import FollowerSerializer
from ..serializers.inboxserializer import InboxItemsSerializer, InboxFollowRequestSerializer
from ..api_serializers.author_api_serializer import AuthorAPISerializer
from ..api_serializers.post_api_serializer import PostAPISerializer
from ..serializers.postlikeserializer import PostLikeSerializer
from ..serializers.commentserializer import CommentSerializer
from ..config import *

author_serializer = AuthorSerializer()
author_api_serializer = AuthorAPISerializer()
post_api_serializer = PostAPISerializer()
post_serializer = PostSerializer()
follower_serializer = FollowerSerializer()
post_like_serializer = PostLikeSerializer()
# post_comment_serializer = CommentSerializer()

pp = pprint.PrettyPrinter()

class InboxAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def get_inbox_posts_data(self, author, inbox_posts):
        """
        Get inbox posts data.
        Parameters:
            author (Author): Author.
            inbox_posts (list): Inbox posts.
        Returns:
            (dict): Inbox posts data.
        """
        inbox_posts_data = {
            "type": "inbox",
            "author": author.url
        }

        posts_data_list = []

        for post in inbox_posts:
            curr_post_data = post_api_serializer.get_post_data(post)
            del(curr_post_data["commentsSrc"])
            posts_data_list.append(curr_post_data)
        
        inbox_posts_data["items"] = posts_data_list

        return inbox_posts_data
    
    def get_all_inbox_posts(self, author_id, page=None, size=None, data_type=None):
        """
        Get all inbox posts for an author.
        Parameters:
            author_id (uuid): Author id.
            page (int): Page number.
            size (int): Number of items per page.
            data_type (str): Type of data to return.
        Returns:
            (dict, int): Serialized data and status code.        
        """
        if not author_serializer.author_exists(author_id):
            return {"msg": "Author does not exist."}, 404
        
        author = author_serializer.get_author_by_id(author_id)
        inbox_items = []

        # Get all inbox posts.
        if data_type == "post":
            inbox = author.inbox.all().filter(type="post")    
            inbox_items = [inbox_obj.content_object for inbox_obj in inbox]
        
        # Get all inbox follow requests.
        if data_type == "request":
            inbox = author.inbox.all().filter(type="follow")
            if inbox != []:
                inbox_items = [inbox_obj.content_object.from_author for inbox_obj in inbox if inbox_obj.content_object.approved == False]

        # Paginate inbox items.
        if page and size:
            paginator = Paginator(inbox_items, size)
            inbox_items = paginator.get_page(page)

        # Serialize inbox items based on type.
        if data_type == "post":
            post_serializer = PostSerializer(inbox_items, many=True)
            serializer = InboxItemsSerializer(data={
                        'page': page,
                        'size': size,
                        'items': post_serializer.data
                    })
            # Return serialized data.
            if serializer.is_valid():
                return serializer.data, 200
            else:
                return serializer.errors, 400
        elif data_type == "request":
            a_serializer = AuthorSerializer(inbox_items, many=True)
            serializer = InboxFollowRequestSerializer(data={
                        'page': page,
                        'size': size,
                        'items': a_serializer.data
                    })
            # Return serialized data.
            if serializer.is_valid():
                return serializer.data, 200
            else:
                return serializer.errors, 400
    
    def handle_post(self, author_id, request_data, auth_header):
        """
        Handle post request send to inbox.
        Parameters:
            author_id (uuid): Author id.
            request_data (dict): Request data.
            auth_header (str): Authorization header.
        Returns:
            (dict, int): Serialized data and status code.
        """
        if not author_serializer.author_exists(author_id):
            return {"msg": "Author does not exist."}, 404
        
        author = author_serializer.get_author_by_id(author_id)

        serializer = PostSerializer(data=request_data)
        if serializer.is_valid():
            # TODO: Validate post_id is a UUID
            # Get post author id.
            post_id_url = urlparse(request_data["id"]).path.rstrip("/").split('/')
            foreign_author_id = uuid.UUID(post_id_url[-3])
            post_id = post_id_url[-1]
            
            # Check if current author is followed by foreign author to receive posts.
            if author_id != foreign_author_id and not follower_serializer.follower_exists(foreign_author_id, author_id):
                return {"msg": f"{author_id} is not following author: {foreign_author_id}"}, 400

            method = ""
            # Check if post exists to send POST or PUT request.
            if post_serializer.post_exists(foreign_author_id, post_id):
                method = "POST"
            else:
                method = "PUT"

            # Create or update post.
            url = f"{BASE_HOST}/authors/{foreign_author_id}/posts/{post_id}/"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"{auth_header}"
            }

            res = requests.request(method=method, url=url, headers=headers, data=json.dumps(request_data))

            if res.status_code in [200, 201]:
                post = post_serializer.get_author_post(foreign_author_id, post_id)
                # create new inbox entry referencing the post send to inbox.
                inbox_post = Inbox.objects.create(content_object=post, author=author, type="post")
                inbox_post.save()
                # return {"msg": f"Post has been send to {author_id} inbox"}, 200
                return PostSerializer(post).data, 200
            else:
                return json.loads(res.text), 404
        else: 
            return serializer.errors, 400

    
    def handle_follow_request(self, author_id, request_data, auth_header):
        follow_serializer = FollowerSerializer(data=request_data)
        
        if follow_serializer.is_valid():
            validated_data = follow_serializer.validated_data
            
            # get post author id 
            actor_id_path = urlparse(request_data["actor"]["id"]).path.rstrip("/").split('/')
            foreign_author_id = uuid.UUID(actor_id_path[-1])

            # If local author recives a follow request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"{auth_header}"
                }
            url = f"{BASE_HOST}/authors/{author_id}/followers/{foreign_author_id}/"

            approved = False

            # If local author gets a response of request being approved
            if author_id == foreign_author_id:
                actor_id_path = urlparse(request_data["object"]["id"]).path.rstrip("/").split('/')
                foreign_author_id = uuid.UUID(actor_id_path[-1])

                # Check if local author has not send a follow request
                if not follow_serializer.follower_exists(foreign_author_id, author_id):
                    return {"msg": f"{author_id} has not send a follow request to you."}, 400

                url = f"{BASE_HOST}/authors/{foreign_author_id}/followers/{author_id}/"
                request_data["approved"] = True
                approved = True

            res = requests.request(method="PUT", url=url, headers=headers, data=json.dumps(request_data))
            if res.status_code in [200, 201]:
                # create new inbox entry
                author = author_serializer.get_author_by_id(author_id)
                follow = None
                if approved:
                    follow = follow_serializer.get_relation_by_ids(foreign_author_id, author_id)
                else: 
                    follow = follow_serializer.get_relation_by_ids(author_id, foreign_author_id)
                inbox_post = Inbox.objects.create(content_object=follow, author=author, type="follow")
                inbox_post.save()
                if approved:
                    return {"msg": f"Approved. {author_id} is following {foreign_author_id}."}, 200
                return {"msg": f"Follow request has been send to {author_id} inbox"}, 200
            else:
                return json.loads(res.text), res.status_code
        else:
            return follow_serializer.errors, 400
        
    def handle_like_request(self, author_id, request_data):
        try:
            if not author_serializer.author_exists(author_id):
                return {"msg": "Author does not exist."}, 404
        
            author = author_serializer.get_author_by_id(author_id)

            post_like_serializer = PostLikeSerializer(data=request_data)

            if post_like_serializer.is_valid():
                validated_data = post_like_serializer.validated_data

                foreign_author_id = urlparse(request_data["author"]["id"]).path.split('/')[-1]
                foreign_author = author_serializer.get_author_by_id(foreign_author_id)

                validated_data["author"] = foreign_author

                post_id_url = urlparse(request_data["object"]).path.rstrip('/').split('/')
                post_id = post_id_url[-1]
                post = post_serializer.get_author_post(author_id, post_id)
                validated_data["post"] = post
                post_like_object = post_like_serializer.save()
                
                inbox_post = Inbox.objects.create(content_object=post_like_object, author=author, type="like")
                inbox_post.save()

                return "Like has been added to the author post", 200 
            else:
                return post_like_serializer.errors, 400
        except Exception as e:
            return str(e), 500
    
    def handle_comment_request(self, author_id, request_data):
        try:
            if not author_serializer.author_exists(author_id):
                return {"msg": "Author does not exist."}, 404
        
            author = author_serializer.get_author_by_id(author_id)

            post_comment_serializer = CommentSerializer(data=request_data)

            if post_comment_serializer.is_valid():
                validated_data = post_comment_serializer.validated_data

                foreign_author_id = urlparse(request_data["author"]["id"]).path.split('/')[-1]
                foreign_author = author_serializer.get_author_by_id(foreign_author_id)
                validated_data["author"] = foreign_author

                post_id_url = urlparse(request_data["object"]).path.rstrip('/').split('/')
                post_id = post_id_url[-1]
                post = post_serializer.get_author_post(author_id, post_id)
                validated_data["post"] = post
                post_comment_object = post_comment_serializer.save()
                
                inbox_post = Inbox.objects.create(content_object=post_comment_object, author=author, type="comment")
                inbox_post.save()

                return "Comment has been added to the author post", 200
            else:
                return "Comment has not been added to the author post", 400
        except Exception as e:
            return str(e), 500