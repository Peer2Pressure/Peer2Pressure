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

# Local Libraries
from .. import utils
from ..models import *
from ..serializers.postserializer import PostSerializer
from ..api_serializers.post_api_serializer import PostAPISerializer

# API serializer
post_api_serializer = PostAPISerializer()

class SinglePostAPI(GenericAPIView):
    serializer_class = PostSerializer

    def get(self, request, author_id, post_id):
        post = post_api_serializer.get_single_post(author_id, post_id)
        if post:
            return Response(post)
        return Response(data={"msg": "Unable to get post."}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, author_id, post_id):
        # if request.user.is_authenticated:
        #     pass
        # else:
        #     pass

        post = post_api_serializer.add_new_post(author_id, request.data, post_id=post_id)
        if post:
            return Response(post)
        return Response(data={"msg": "Unable to create post"}, status=status.HTTP_404_NOT_FOUND)

    
    # must be authenticated
    def post(self, request, author_id, post_id):
        updated_post = post_api_serializer.update_author_post(author_id, post_id, request.data)
        if updated_post:
            return Response(updated_post)
        return Response(data={"msg": "Unable to update post"}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, author_id, post_id):
        post = post_api_serializer.delete_author_post(author_id, post_id)
        if post:
            return Response({"msg": f"Post: {post_id} has be deleted"})
        return Response(data={"msg": "Unable to delete post"}, status=status.HTTP_404_NOT_FOUND)


class PostAPI(GenericAPIView):
    serializer_class = PostSerializer

    def get(self, request, author_id):
        try:
            page, size = utils.get_pagination_variables(request.query_params)
        except ValidationError:
            return Response(data={"msg": "Invalid query parameters."}, status=status.HTTP_400_BAD_REQUEST)

        posts = post_api_serializer.get_all_author_posts(author_id, page, size)
        if posts:
            return Response(posts)
        
        return Response(data={"msg": "Unable to get post."}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, author_id):
        post = post_api_serializer.add_new_post(author_id, request.data)
        if post:
            return Response(post)
        return Response(data={"msg": "Unable to create post"}, status=status.HTTP_404_NOT_FOUND)
