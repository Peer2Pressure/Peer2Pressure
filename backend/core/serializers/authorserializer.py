# Local libraries
from .. models import Author

# Third-party libraries
from rest_framework import serializers
from varname import nameof


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def create_author(self, username, firstname, lastname, email, password, host = None, id = None):

        defaults = {
            nameof(Author.username): username,
            nameof(Author.first_name): firstname,
            nameof(Author.last_name): lastname,
            nameof(Author.email): email,
            nameof(Author.password): password
        }

        if id is not None:
            try:
                author_obj = self.get_author_by_id(id)
            except ValueError:
                defaults[Author.id] = id

        if host is not None:
            defaults[nameof(Author.host)] = host

        author_obj= Author.objects.create(**defaults)

        return author_obj.id
    
    def get_author_id_by_username(self, username):
        try:
            author_obj = Author.objects.get(username=username)
        except Author.DoesNotExist:
            raise ValueError("Author does not exist")

        return author_obj.id

    def get_author_by_id(self, author_id):

        try:
            author_obj = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            raise ValueError("Author does not exist")
        
        return author_obj
    
    def update_author(self, author_id, request_data):
        author = None
        updatable_fields = ["first_name", "last_name", "username", "email", "avatar"]
        try:
            author = self.get_author_by_id(author_id=author_id)
        except ValueError:
            return None

        defaults = {}
        for key in request_data:
            if key in updatable_fields:
                defaults[key] = request_data[key]
        
        print(defaults)

        Author.objects.filter(pk=author_id).update(**defaults)

        return self.get_single_author(author_id)
    
    def get_author_data(self, author):
        author_data = {
            "type": "author",
            "id": author.id,
            "url": author.url,
            "host": author.host,
            "displayName": f"{author.first_name} {author.last_name}",
            "username": author.username,
            "email": author.email,
            "profileImage": f"{author.host}{author.avatar.url}",
            }
        
        return author_data


    def get_single_author(self, author_id):
        author_data = {}
        try:
            author = self.get_author_by_id(author_id)
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