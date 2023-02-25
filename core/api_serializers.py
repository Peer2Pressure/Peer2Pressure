from rest_framework import serializers
from . models import *
from varname import nameof
from .serializers.authorserializer import AuthorSerializer

author_serializer = AuthorSerializer()

class AuthorAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def get_single_author(self, author_id):
        author_obj = author_serializer.get_author_by_id(author_id)

        result_dict = {
            "type": "author",
            "host": author_obj.host,
            "displayName": author_obj.username,
            "github": author_obj.email
        }

        id = str(author_obj.host) + "authors/" + str(author_id)

        result_dict["id"] = id

        result_dict["url"] = id

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