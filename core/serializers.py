# Local libraries
from . models import Author

# Third-party libraries
from rest_framework import serializers
from varname import nameof


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def create_author(self, username, firstname, lastname, email, password):
        identifiers = {
            nameof(Author.username): username,
        }

        defaults = {
            nameof(Author.first_name): firstname,
            nameof(Author.last_name): lastname,
            nameof(Author.email): email,
            nameof(Author.password): password
        }

        author_obj, author_created = Author.objects.create(**identifiers, defaults=defaults)

        return author_obj, author_created