from rest_framework import serializers
from . models import *
from varname import nameof
from .serializers.authorserializer import AuthorSerializer
from .serializers.relationserializer import RelationSerializer
from .serializers.postserializer import PostSerializer

author_serializer = AuthorSerializer()
relation_serializer = RelationSerializer()
post_serializer = PostSerializer()

class AuthorAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def get_single_author(self, author_id):
        author_obj = author_serializer.get_author_by_id(author_id)

        result_dict = {
            "type": "author",
            "id": author_id,
            "host": author_obj.host,
            "first_name": author_obj.first_name,
            "last_name": author_obj.last_name,
            "username": author_obj.username,
            "email": author_obj.email,
            "avatar": author_obj.avatar.url,
        }

        url = str(author_obj.host) + "authors/" + str(author_id)
        # result_dict["id"] = id
        result_dict["url"] = url
        
        return result_dict

    # def update_single_author(self, author_id):
    #     updated_author = author_serializer.update(author_id)

    #     return updated_author

        return result_dict
    
    def get_all_authors(self):

        authors = author_serializer.all_authors()

        result_dict = {}

        result_dict["type"] = "authors"

        list_authors = []

        for author in authors:

            # TODO: Need to add image
            curr_author = {}

            curr_author["type"] = "author"
            curr_author["id"] = str(author.host) + "authors/" + str(author.id)
            curr_author["url"] = str(author.host) + "authors/" + str(author.id)
            curr_author["host"] = author.host
            curr_author["displayName"] = author.username
            curr_author["github"] = author.email

            list_authors.append(curr_author)

        result_dict["items"] = list_authors

        return result_dict
    

class RelationAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = "__all__"

    def get_all_followers(self, author_id):

        followers = relation_serializer.get_followers(author_id)

        if len(followers) <= 0:
            return {"type": "followers", "items": []}
        
        result_dict = {}
        result_dict["type"] = "followers"

        list_authors = []

        for author in followers:

            # TODO: Need to add image
            curr_author = {}

            curr_author["type"] = "author"
            curr_author["id"] = str(author.host) + "authors/" + str(author.id)
            curr_author["url"] = str(author.host) + "authors/" + str(author.id)
            curr_author["host"] = author.host
            curr_author["displayName"] = author.username
            curr_author["github"] = author.email

            list_authors.append(curr_author)

        result_dict["items"] = list_authors

        return result_dict


author_api_serializer = AuthorAPISerializer()

class PostAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def get_a_post(self, authorid, postid):
        result_dict = {}

        result_dict["type"] = "post"
        # TODO: Need to add title to POST Model
        result_dict["title"] = ""

        # TODO: Need to handle the case if post or author doesn't exist
        post_obj = post_serializer.get_post(authorid, postid)
        author_obj = author_serializer.get_author_by_id(authorid)

        result_dict["id"] = str(author_obj.host) + "/authors/" + str(authorid) + "/posts/" + str(postid)

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
