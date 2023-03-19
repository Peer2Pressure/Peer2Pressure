# Third-party libraries
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Local libraries
from .. import utils
from ..models import *
from ..serializers.authorserializer import AuthorSerializer
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
        except ValidationError:
            return None
        
        inbox_posts = author.inbox_posts.all()

        inbox_posts_data = self.get_inbox_posts_data(author, inbox_posts)

        return inbox_posts_data

