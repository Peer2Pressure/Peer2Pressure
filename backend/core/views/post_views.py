# Built-in libraries
import json

# Third-party libraries
# from django.http import HttpResponse, JsonResponse
# from rest_framework import authentication, permission

# Third-party libraries
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Local Libraries
from .. import utils
from ..models import *
from ..serializers.postserializer import PostSerializer, AllPostSerializer
from ..api_serializers.post_api_serializer import PostAPISerializer

# API serializer
post_api_serializer = PostAPISerializer()

class SinglePostAPI(GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Posts'])
    def get(self, request, author_id, post_id):
        post = post_api_serializer.get_single_post(author_id, post_id)
        if post:
            return Response(post)
        return Response(data={"msg": "Unable to get post."}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(tags=['Posts'])
    def put(self, request, author_id, post_id):
        post, code = post_api_serializer.add_new_post(author_id, request.data, post_id=post_id)
        if code == 201:
            return Response(post, status=status.HTTP_201_CREATED)
        elif code == 400:
            return Response(post, status=status.HTTP_400_BAD_REQUEST)
        elif code == 404:
            return Response(post, status=status.HTTP_404_NOT_FOUND)
    
    # must be authenticated
    @swagger_auto_schema(tags=['Posts'])
    def post(self, request, author_id, post_id):
        post, code = post_api_serializer.update_author_post(author_id, post_id, request.data)
        if code == 200:
            return Response(post, status=status.HTTP_200_OK)
        elif code == 400:
            return Response(post, status=status.HTTP_400_BAD_REQUEST)
        elif code == 404:
            return Response(post, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(tags=['Posts'])
    def delete(self, request, author_id, post_id):
        post = post_api_serializer.delete_author_post(author_id, post_id)
        if post:
            return Response({"msg": f"Post: {post_id} has been deleted"})
        return Response(data={"msg": "Unable to delete post"}, status=status.HTTP_404_NOT_FOUND)


class PostAPI(GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Posts'],
        operation_description='Get all posts for an author.',
        responses={
        200: openapi.Response(
            description='OK',
            schema=AllPostSerializer()
            )   
        }
    )
    def get(self, request, author_id):
        try:
            page, size = utils.get_pagination_variables(request.query_params)
        except ValidationError:
            return Response(data={"msg": "Invalid query parameters."}, status=status.HTTP_400_BAD_REQUEST)

        posts, code = post_api_serializer.get_all_author_posts(author_id, page, size)

        if code == 200:
            return Response(posts, status=status.HTTP_200_OK)
        elif code == 400:
            return Response(posts, status=status.HTTP_400_BAD_REQUEST)
        elif code == 404:
            return Response(posts, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
            tags=['Posts'],
            operation_description='Create a new post.',)
    def post(self, request, author_id):
        post, code = post_api_serializer.add_new_post(author_id, request.data)
        if code == 201:
            return Response(post, status=status.HTTP_201_CREATED)
        elif code == 400:
            return Response(post, status=status.HTTP_400_BAD_REQUEST)
        elif code == 404:
            return Response(post, status=status.HTTP_404_NOT_FOUND)
    