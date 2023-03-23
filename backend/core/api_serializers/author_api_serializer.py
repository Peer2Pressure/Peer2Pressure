# Third-party libraries
from django.core.paginator import Paginator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


# Local libraries
from .. import utils
from ..models import *
from ..serializers.authorserializer import AuthorSerializer, AllAuthorSerializer

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
        except ValidationError:
            return None
        
        serializer = AuthorSerializer(author)

        return serializer.data
    
    def get_all_authors(self, page=None, size=None):
        authors = Author.objects.all()
        
        if page and size:
            paginator = Paginator(authors, size)
            authors = paginator.get_page(page)

        authors_serializer = AuthorSerializer(authors, many=True)
        
        serializer = AllAuthorSerializer(data={
                        'type': 'authors',
                        'page': page,
                        'size': size,
                        'items': authors_serializer.data
                    })

        if serializer.is_valid():
            return serializer.data, 1
        else:
            return serializer.errors, 0

    def update_author(self, author_id, request_data):
        try:
            author = author_serializer.get_author_by_id(author_id=author_id)
        except ValidationError:
            # TODO : If author does not exist create new author. Will need to create new User object too !!!
            # author = author_serializer.create_author()
            return None, None
        serializer = AuthorSerializer(author, request_data)
        
        if serializer.is_valid():
            serializer.save()
            # serializer.update(author, serializer.validated_data)
            return serializer.data, 1
        else:
            return serializer.errors, 0
