# Built-in libraries
import json

# Third-party libraries
# from django.http import HttpResponse, JsonResponse
# from rest_framework import authentication, permission
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Local Libraries
from .. import utils
from ..api_serializers.author_api_serializer import AuthorAPISerializer
from ..serializers.authorserializer import AuthorSerializer, AllAuthorSerializer
from ..models import *

# author_list_serializer = AuthorListSerializer()
author_api_serializer = AuthorAPISerializer()

@permission_classes([IsAuthenticated])
def get_author_id(request):
    author_id = request.user.author_profile.m_id
    return JsonResponse({'author_id': author_id})

# def redirect_authorlist_api(request):
#     # Get the current URL and headers
#     current_url = request.build_absolute_uri()
#     headers = dict(request.headers.items())
    
#     # Redirect to the new endpoint with all headers and query parameters
#     new_url = 'https://example.com/new-endpoint'
#     return redirect(new_url, permanent=False, **headers)

class AuthorListAPI(GenericAPIView):
    serializer_class = AllAuthorSerializer
    permission_classes = [IsAuthenticated]

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
        try:
            page, size = utils.get_pagination_variables(request.query_params)
        except ValidationError:
            return Response(data={"msg": "Invalid query parameters."}, status=status.HTTP_400_BAD_REQUEST)

        authors, _ = author_api_serializer.get_all_authors(page, size)
        if _:
            return Response(authors, status=status.HTTP_200_OK)
        return Response(authors, status=status.HTTP_404_NOT_FOUND)

class AuthorAPI(GenericAPIView):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
            tags=['Authors'],
            operation_description='Get a single author.',)
    def get(self, request, author_id):        
        author = author_api_serializer.get_single_author(author_id)
        if author:
            return Response(author)
        return Response(data={"msg": "Author does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
            tags=['Authors'],
            operation_description='Update a single author.',)
    def post(self, request, author_id):
        update_author, _ = author_api_serializer.update_author(author_id, request.data)
        
        if _:
            return Response(update_author, status=status.HTTP_200_OK)
        elif _ == 0:
            return Response(update_author, status=status.HTTP_400_BAD_REQUEST)
        elif _ is None:
            return Response(data={"msg": "Author does not exist."}, status=status.HTTP_404_NOT_FOUND)
