import requests
from urllib.parse import urlparse

# Third-party libraries
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Local libraries
from .. import utils
from ..models import *
from ..serializers.authorserializer import AuthorSerializer
from ..serializers.postserializer import PostSerializer
from ..api_serializers.author_api_serializer import AuthorAPISerializer
from ..api_serializers.post_api_serializer import PostAPISerializer

author_serializer = AuthorSerializer()
author_api_serializer = AuthorAPISerializer()
post_api_serializer = PostAPISerializer()

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
    
    def save_post(self, author_id, request_data):
        try:
            author = author_serializer.get_author_by_id(author_id)
        except ValidationError as e:
            return {"msg": str(e)}, 404

        # get post author id 
        post_id_url = urlparse(request_data["id"]).path.split('/')
        post_id = post_id_url[4]

        url = f"http://localhost:8000/authors/{author_id}/posts/{post_id}"
        res = requests.post(url, data=request_data)
        print(res.status_code)

        return {"msg": f"Post has been send to {author_id} inbox"}, 201
        # serializer = PostSerializer(data=request_data)

        # post = None
        # if serializer.is_valid():
        #     validated_post_data = serializer.validated_data
        #     print(validated_post_data["id"])

        #     # get post author id 
        #     post_id_url = urlparse(validated_post_data["id"]).path.split('/')
        #     post_author_id = post_id_url[2]
        #     print(post_author_id)
            
            # # validate current author follows post author
            # url = f"http://localhost:8000/authors/{post_author_id}/followers/{author_id}"
            # res = requests.get(url)
            # print("res: ", res)
            # if res != 200:
            #     return None, res.status_code
            
            # create new post for post_author
            

            
            # print(res.text)

            # try:
            #     post_author_obj = author_serializer.get_author_by_id(post_author_id)
            # except ValidationError as e:
            #     return {"msg": str(e)}, 404
            
            # validated_post_data["author"] = post_author_obj
            # print(validated_post_data)

            # post = serializer.create(validated_post_data)
            # post.save()

            

        #     return {"msg": f"Post has been send to {author_id} inbox"}, 201
        # else:
        #     return serializer.errors, 400
        
        
