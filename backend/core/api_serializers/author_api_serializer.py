# Third-party libraries
from rest_framework import serializers

# Local libraries
from ..models import *
from ..serializers.authorserializer import AuthorSerializer

author_serializer = AuthorSerializer()

class AuthorAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def get_author_data(self, author):
        author_data = {
            "type": "author",
            "id": author.id,
            "url": author.url,
            "host": author.host,
            "displayName": f"{author.first_name} {author.last_name}",
            "username": author.username,
            "email": author.email,
            "profileImage": author.avatar,
            }
        return author_data
    
    def get_single_author(self, author_id):
        author_data = {}
        try:
            author = author_serializer.get_author_by_id(author_id)
            author_data = self.get_author_data(author)
        except ValueError:
            return None
        return author_data
    
    def get_all_authors(self):

        authors = Author.objects.all()
        
        result_dict = {}
        result_dict["type"] = "authors"

        authors_list = []

        for author in authors:
            curr_author_data = self.get_author_data(author)
            authors_list.append(curr_author_data)

        result_dict["items"] = authors_list

        return result_dict

    def create_or_update_author(self, author_id, request_data):
        author = None
        updatable_fields = ["first_name", "last_name", "username", "email", "avatar"]
        try:
            author = author_serializer.get_author_by_id(author_id=author_id)
        except ValueError:
            # TODO : If author does not exist create new author. Will need to create new User object too !!!
            # author = author_serializer.create_author()
            return None

        defaults = {}
        for key in request_data:
            if key in updatable_fields:
                defaults[key] = request_data[key]

        Author.objects.filter(pk=author_id).update(**defaults)

        return self.get_single_author(author_id)