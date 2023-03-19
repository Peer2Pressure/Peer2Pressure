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
from ..serializers.authorserializer import AuthorSerializer, AllAuthorSerializer
from ..models import *
from drf_yasg import openapi


# author_list_serializer = AuthorListSerializer()
author_api_serializer = AuthorAPISerializer()

class CurrentAuthorID(GenericAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        print("USER:   ",request.user)
        author_id = request.user.author_profile.id
        return Response({'author_id': author_id})
        

class AuthorListAPI(GenericAPIView):
    serializer_class = AllAuthorSerializer

    @swagger_auto_schema(
        tags=['Authors'],
        operation_description='Get all authors.',
        responses={
        200: openapi.Response(
            description='OK',
            schema=AllAuthorSerializer()
            )   
        }
    )
    def get(self, request):
        print(request)
        try:
            page, size = utils.get_pagination_variables(request.query_params)
        except ValidationError:
            return Response(data={"msg": "Invalid query parameters."}, status=status.HTTP_400_BAD_REQUEST)

        authors, _ = author_api_serializer.get_all_authors(page, size)

        # a = Author.objects.all()
        # serializer = AllAuthorSerializer(a)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        
        if _:
            return Response(authors, status=status.HTTP_200_OK)
        return Response(authors, status=status.HTTP_400_BAD_REQUEST)

class AuthorAPI(GenericAPIView):
    serializer_class = AuthorSerializer

    @swagger_auto_schema(tags=['Authors'])
    def get(self, request, author_id):
        author = author_api_serializer.get_single_author(author_id)
        if author:
            return Response(author)
        return Response(data={"msg": "Author does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    # discuss if we need to change to PUT request
    @swagger_auto_schema(tags=['Authors'])
    def post(self, request, author_id):
        update_author = author_api_serializer.update_author(author_id, request.data)
        
        if update_author:
            return Response(update_author)
        return Response(data={"msg": "Author does not exist."}, status=status.HTTP_404_NOT_FOUND)