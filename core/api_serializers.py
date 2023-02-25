from rest_framework import serializers
from . models import *
from . serializers import *
from varname import nameof

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