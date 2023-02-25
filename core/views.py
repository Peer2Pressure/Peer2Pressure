# Local Libraries
# from .serializers import AuthorSerializer
from .serializers.authorserializer import AuthorSerializer
from .models import Author, Relation

# Built-in libraries
import json

# Third-party libraries
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from varname import nameof

def index(request):
    return render(request, "index.html")

class AuthorListAPI(GenericAPIView):
    serializer_class = AuthorSerializer

    def get(self, request):
        authors = Author.objects.all()    
        serializer = AuthorSerializer(authors, many=True)
        data = list(serializer.data)
        return Response(data)

class AuthorAPI(GenericAPIView):
    serializer_class = AuthorSerializer

    def get(self, request, author_id):
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)    
        serializer = AuthorSerializer(author)
        return Response(serializer.data)
    
    # discuss if we need to change to PUT request
    def post(self, request, author_id):
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)    
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class FollowerListAPI(GenericAPIView):
    serializer_class = AuthorSerializer

    def get(self, request, author_id):
        try:
            followers = list(Relation.objects.filter(from_author=author_id, to_author_request=True).values_list('to_author', flat=True))
            followers += list(Relation.objects.filter(to_author=author_id, from_author_request=True).values_list('from_author', flat=True))

            authors = Author.objects.filter(pk__in=list(followers))
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)
        
