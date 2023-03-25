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
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse

# Local Libraries
from .helpers import server_request_authenticated
from .. import utils
from ..models import *
from ..serializers.postserializer import PostSerializer, AllPostSerializer
from ..api_serializers.post_api_serializer import PostAPISerializer
from ..config import *

# API serializer
post_api_serializer = PostAPISerializer()

class SinglePostAPI(GenericAPIView):
    serializer_class = PostSerializer

    @swagger_auto_schema(tags=['Posts'])
    def get(self, request, author_id, post_id):
        current_host = f"{request.scheme}://{request.get_host()}"
        
        if current_host != BASE_HOST and not server_request_authenticated(request):
            response = HttpResponse("Authorization required.", status=401)
            response['WWW-Authenticate'] = 'Basic realm="Authentication required"'
            return response

        post = post_api_serializer.get_single_post(author_id, post_id)
        if post:
            return Response(post)
        return Response(data={"msg": "Unable to get post."}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(tags=['Posts'])
    def put(self, request, author_id, post_id):
        # if request.user.is_authenticated:
        #     pass
        # else:
        #     pass
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
        ALLOWED_IPS = ["68.151.70.49"]
        print("originating host", request.get_host())
        originating_host = request.META.get('HTTP_X_FORWARDED_FOR', '').split(",")[0].strip()
        print("IP: ", originating_host)
        current_host = f"{request.scheme}://{request.get_host()}"
        
        if originating_host not in ALLOWED_IPS and not server_request_authenticated(request):
            response = HttpResponse("Authorization required.", status=401)
            response['WWW-Authenticate'] = 'Basic realm="Authentication required"'
            return response
        
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
    