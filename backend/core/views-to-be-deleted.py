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
from .api_serializers import *
from .serializers.commentserializer import CommentSerializer
from .serializers.likeserializer import LikeSerializer
from .models import *



class LikeAPI(GenericAPIView):
    serializer_class = LikeSerializer

    def get(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=author_id)
            post = Post.objects.get(pk=post_id)
            likes = post.likes
        except (Author.DoesNotExist, Post.DoesNotExist, Like.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LikeSerializer(likes, many=True)
        data = list(serializer.data)
        return Response(data)
    
    def post(self, request, author_id, post_id):
        comment = request.data["comment"]
        new_comment = CommentSerializer.create_comment(author_id=author_id, post_id=post_id, comment=comment)
        if new_comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(new_comment)
        return Response(serializer.data)

class LikedAPI(GenericAPIView):
    serializer_class = LikeSerializer
    
    def get(self, request, author_id):
        try:
            author = Author.objects.get(pk=author_id)
            likes = author.likes
        except (Author.DoesNotExist, Like.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Like(likes, many=True)
        data = list(serializer.data)
        return Response(data)

# incomplete
class CommentLikeAPI(GenericAPIView):
    serializer_class = LikeSerializer

    def get(sef, request, author_id, post_id, comment_id):
        try:
            author = Author.objects.get(pk=author_id)
            post = Post.objects.get(pk=post_id)
            comment = Comment.objects.get(pk=comment_id)
        except (Author.DoesNotExist, Post.DoesNotExist, Comment.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        # serializer = LikeSerializer(likes, many=True)
        # data = list(serializer.data)
        # return Response(data)
        return None


class InboxLike(GenericAPIView):

    def post(self, request, author_id):
        pass
