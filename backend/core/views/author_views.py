# Built-in libraries
import json

# Third-party libraries
# from django.http import HttpResponse, JsonResponse
# from rest_framework import authentication, permission
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

# Local Libraries
from .. import utils
from ..api_serializers.author_api_serializer import AuthorAPISerializer
from ..serializers.authorserializer import AuthorSerializer


author_serializer = AuthorSerializer()
author_api_serializer = AuthorAPISerializer()

class CurrentAuthorID(GenericAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("USER:   ",request.user)
        author_id = request.user.author_profile.id
        return Response({'author_id': author_id})
        

class AuthorListAPI(GenericAPIView):
    serializer_class = AuthorSerializer

    def get(self, request):
        try:
            page, size = utils.get_pagination_variables(request.query_params)
        except ValidationError:
            return Response(data={"msg": "Invalid query parameters."}, status=status.HTTP_400_BAD_REQUEST)

        authors = author_api_serializer.get_all_authors(page, size)
        return Response(authors)

class AuthorAPI(GenericAPIView):
    serializer_class = AuthorSerializer
    
    def get(self, request, author_id):
        author = author_api_serializer.get_single_author(author_id)
        if author:
            return Response(author)
        return Response(data={"msg": "Author does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    # discuss if we need to change to PUT request
    def post(self, request, author_id):
        update_author = author_api_serializer.update_author(author_id, request.data)
        
        if update_author:
            return Response(update_author)
        return Response(data={"msg": "Author does not exist."}, status=status.HTTP_404_NOT_FOUND)