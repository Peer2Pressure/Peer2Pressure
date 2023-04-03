from urllib.parse import urlparse

# Third-party libraries
from django.core.paginator import Paginator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


# Local libraries
from .. import utils
from ..models import *
from ..serializers.authorserializer import AuthorSerializer, AllAuthorSerializer
from ..config import *

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
        all_authors = Author.objects.all()
        
        authors = []
        for author in all_authors:
            if urlparse(author.host).hostname == urlparse(BASE_HOST).hostname:
                authors.append(author)

        print("AUTHORS:  ", len(authors))

        if page and size:
            paginator = Paginator(authors, size)
            print(paginator.num_pages)
            # print(type(paginator.num_pages))
            if page > paginator.num_pages:
                return {}, 0
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
        # serializer = AuthorSerializer(request_data)
        updated_serializer = AuthorSerializer(author, request_data)
        if updated_serializer.is_valid():
            validated_data = updated_serializer.validated_data
            # print(serializer.validated_data)
            updated_serializer.save()
            # serializer.update(author, serializer.validated_data)
            return updated_serializer.data, 1
        else:
            return updated_serializer.errors, 0
