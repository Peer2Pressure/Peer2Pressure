import requests
import json
from urllib.parse import urlparse
import uuid
import pprint

# Third-party libraries
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Local libraries
from .. import utils
from ..models import *
from ..serializers.authorserializer import AuthorSerializer
from ..serializers.postserializer import PostSerializer
from ..serializers.followerserializer import FollowerSerializer
from ..api_serializers.author_api_serializer import AuthorAPISerializer
from ..api_serializers.post_api_serializer import PostAPISerializer

author_serializer = AuthorSerializer()
author_api_serializer = AuthorAPISerializer()
post_api_serializer = PostAPISerializer()
post_serializer = PostSerializer()

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
        try:
            author = author_serializer.get_author_by_id(author_id)
        except ValidationError as e:
            return {"msg": str(e)}, 404 
        
        inbox_posts = author.inbox_posts.all()

        inbox_posts_data = self.get_inbox_posts_data(author, inbox_posts)

        return inbox_posts_data
    
    def handle_post(self, author_id, request_data):
        try:
            author = author_serializer.get_author_by_id(author_id)
        except ValidationError as e:
            return {"msg": str(e)}, 404

        # TODO: Validate post_id is a UUID
        # get post author id
        post_id_url = urlparse(request_data["id"]).path.split('/')
        post_id = post_id_url[4]

        try:
            existing_post = post_serializer.get_author_post(author_id, post_id)
            method = "POST"
        except ValidationError:
            method = "PUT"

        url = f"http://localhost:8000/authors/{author_id}/posts/{post_id}/"
        # print(method, url)
        headers = {"Content-Type": "application/json"}
        res = requests.request(method=method, url=url, headers=headers, data=json.dumps(request_data))

        print(type(res.status_code))

        if res.status_code in [200, 201]:
            # create new inbox entry
            post = post_serializer.get_author_post(author_id, post_id)
            inbox_post = Inbox.objects.create(content_object=post, author=author, type="post")
            # print()
            # print("INBOX:         ",inbox_post)
            # print(inbox_post.content_object)
            inbox_post.save()
            return {"msg": f"Post has been send to {author_id} inbox"}, 200
        else:
            return json.loads(res.text), 404
    
    def handle_follow_request(self, author_id, request_data):
        print("ASdasdsadasdsa")
        # print(request_data)
        if not author_serializer.author_exists(author_id):
            return {"msg": "Author does not exist."}, 404
            
        # pp.pprint(request_data)

        follow_serializer = FollowerSerializer(data=request_data)
        
        
        if follow_serializer.is_valid():
            pp.pprint(follow_serializer.data)
            # print(follow_serializer.validated_data)
            # get post author id 
            actor_id_path = urlparse(request_data["actor"]["id"]).path.split('/')
            actor_id = actor_id_path[2]
            # actor_id = None
            # if len(actor_id_path) >= 3:
            #     actor_id_str = actor_id_path[2]
            #     try:
            #         actor_id = uuid.UUID(actor_id_str)
            #     except ValueError:
            #         return {"msg": "Invalid actor id"}
            headers = {"Content-Type": "application/json"}
            url = f"http://localhost:8000/authors/{author_id}/followers/{actor_id}/"

            res = requests.request(method="PUT", url=url, headers=headers, data=json.dumps(request_data))

            # pp.pprint(res.text)
        
        return {"msg": "follower"}, 200