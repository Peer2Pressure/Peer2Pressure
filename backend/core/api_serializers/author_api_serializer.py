# Third-party libraries
from rest_framework import serializers

# Local libraries
from .. import utils
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
            "displayName": f"{author.name}",
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
    
    def get_all_authors(self, page=None, size=None):

        authors = Author.objects.all()
        
        result_dict = {}
        result_dict["type"] = "authors"

        authors_list = []

        for author in authors:
            curr_author_data = self.get_author_data(author)
            authors_list.append(curr_author_data)
        
        if page and size:
            paginated_authors = utils.paginate_list(authors_list, page, size)
            
            result_dict["page"] = page
            result_dict["size"] = size
            result_dict["items"] = paginated_authors
        else:
            result_dict["items"] = authors_list

        return result_dict

    def update_author(self, author_id, request_data):
        author = None
        updatable_fields = ["name", "username", "avatar"]

        try:
            author = author_serializer.get_author_by_id(author_id=author_id)
        except ValueError:
            # TODO : If author does not exist create new author. Will need to create new User object too !!!
            # author = author_serializer.create_author()
            return None

        defaults = {}
        for key in request_data:
            if key == "displayName":
                defaults["name"] = request_data[key]
            elif key == "username":
                defaults["username"] = request_data[key]
            elif key == "profileImage":
                defaults["profileImage"] = request_data[key]
                
        Author.objects.filter(pk=author_id).update(**defaults)

        return self.get_single_author(author_id)