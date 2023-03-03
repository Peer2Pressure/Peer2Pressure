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
