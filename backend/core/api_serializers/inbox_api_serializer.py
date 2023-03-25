import requests
import json
from urllib.parse import urlparse
import uuid
import pprint

# Third-party libraries
from django.core.paginator import Paginator

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Local libraries
from .. import utils
from ..models import *
from ..serializers.authorserializer import AuthorSerializer
from ..serializers.postserializer import PostSerializer
from ..serializers.followerserializer import FollowerSerializer
from ..serializers.inboxserializer import InboxItemsSerializer
from ..api_serializers.author_api_serializer import AuthorAPISerializer
from ..api_serializers.post_api_serializer import PostAPISerializer
from ..config import *

author_serializer = AuthorSerializer()
author_api_serializer = AuthorAPISerializer()
post_api_serializer = PostAPISerializer()
post_serializer = PostSerializer()
follower_serializer = FollowerSerializer()


pp = pprint.PrettyPrinter()

class InboxAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def get_inbox_posts_data(self, author, inbox_posts):
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
    
    def get_all_inbox_posts(self, author_id, page=None, size=None):
        if not author_serializer.author_exists(author_id):
            return {"msg": "Author does not exist."}, 404
        
        author = author_serializer.get_author_by_id(author_id)
        
        inbox = author.inbox.all().filter(type="post")
        
        inbox_posts = [inbox_obj.content_object for inbox_obj in inbox]

        if page and size:
            paginator = Paginator(inbox_posts, size)
            inbox_posts = paginator.get_page(page)

        post_serializer = PostSerializer(inbox_posts, many=True)

        serializer = InboxItemsSerializer(data={
                        'page': page,
                        'size': size,
                        'items': post_serializer.data
                    })

        if serializer.is_valid():
            return serializer.data, 200
        else:
            return serializer.errors, 400
    
    def handle_post(self, author_id, request_data):
        if not author_serializer.author_exists(author_id):
            return {"msg": "Author does not exist."}, 404
        
        author = author_serializer.get_author_by_id(author_id)

        serializer = PostSerializer(data=request_data)

        if serializer.is_valid():
            # TODO: Validate post_id is a UUID
            # Get post author id.
            post_id_url = urlparse(request_data["id"]).path.split('/')
            foreign_author_id = uuid.UUID(post_id_url[2])
            post_id = post_id_url[4]

            print("inbox author: ", author_id, "post author: ", foreign_author_id)
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
            headers = {"Content-Type": "application/json"}
            res = requests.request(method=method, url=url, headers=headers, data=json.dumps(request_data))

            if res.status_code in [200, 201]:
                post = post_serializer.get_author_post(foreign_author_id, post_id)
                if method == "PUT":
                    # create new inbox entry referencing the post send to inbox.
                    inbox_post = Inbox.objects.create(content_object=post, author=author, type="post")
                    inbox_post.save()
                # return {"msg": f"Post has been send to {author_id} inbox"}, 200
                return PostSerializer(post).data, 200
            else:
                return json.loads(res.text), 404
        else: 
            return serializer.errors, 400

    
    def handle_follow_request(self, author_id, request_data):
        follow_serializer = FollowerSerializer(data=request_data)
        
        if follow_serializer.is_valid():
            validated_data = follow_serializer.validated_data
            
            # get post author id 
            actor_id_path = urlparse(request_data["actor"]["id"]).path.split('/')
            foreign_author_id = uuid.UUID(actor_id_path[2])

            # If local author recives a follow request
            headers = {"Content-Type": "application/json"}
            url = f"{BASE_HOST}/authors/{author_id}/followers/{foreign_author_id}/"

            approved = False

            # If local author gets a response of request being approved
            if author_id == foreign_author_id:
                actor_id_path = urlparse(request_data["object"]["id"]).path.split('/')
                foreign_author_id = uuid.UUID(actor_id_path[2])

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
        