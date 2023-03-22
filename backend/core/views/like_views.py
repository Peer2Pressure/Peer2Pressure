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
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

# Local Libraries
from ..api_serializers.post_like_api_serializer import PostLikeAPISerializer
from ..api_serializers.comment_like_api_serializer import CommentLikeAPISerializer
from ..models import *

comment_like_api_serializer = CommentLikeAPISerializer()
post_like_api_serializer = PostLikeAPISerializer()

class PostLikeAPI(GenericAPIView):
    serializer_class = PostLikeAPISerializer

    @swagger_auto_schema(tags=['Likes'])
    def get(self, request, author_id, post_id):
        post_likes = post_like_api_serializer.get_all_post_likes(author_id, post_id)
        if post_likes:
            return Response(post_likes)
        return Response(data={"msg": "Unable to get post likes"}, status=status.HTTP_404_NOT_FOUND)


class CommentLikeAPI(GenericAPIView):
    serializer_class = PostLikeAPISerializer
    @swagger_auto_schema(tags=['Likes'])
    def get(self, request, author_id, post_id, comment_id):
        comment_likes = comment_like_api_serializer.get_all_comment_likes(author_id, post_id, comment_id)
        if comment_likes:
            return Response(comment_likes)
        return Response(data={"msg": "Unable to get post likes"}, status=status.HTTP_404_NOT_FOUND)