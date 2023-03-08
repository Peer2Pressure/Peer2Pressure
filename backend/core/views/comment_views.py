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
from ..api_serializers.comment_api_serializer import CommentAPISerializer
from ..serializers.commentserializer import CommentSerializer
from ..models import *

# API serializer
comment_api_serializer = CommentAPISerializer()


class CommentAPI(GenericAPIView):
    serializer_class = CommentSerializer

    def get(self, request, author_id, post_id):
        comments = comment_api_serializer.get_post_comments(author_id, post_id)
        if comments:
            return Response(comments)
        return Response(data={"msg": "Post does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, author_id, post_id):
        comments = comment_api_serializer.add_new_comment(author_id, post_id, request.data)

        comment = request.data["comment"]
        new_comment = CommentSerializer.create_comment(author_id=author_id, post_id=post_id, comment=comment)
        if new_comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(new_comment)
        return Response(serializer.data)

# # incomplete: might have to change to like_vies.py
# class CommentLikeAPI(GenericAPIView):
#     serializer_class = LikeSerializer

#     def get(sef, request, author_id, post_id, comment_id):
#         try:
#             author = Author.objects.get(pk=author_id)
#             post = Post.objects.get(pk=post_id)
#             comment = Comment.objects.get(pk=comment_id)
#         except (Author.DoesNotExist, Post.DoesNotExist, Comment.DoesNotExist):
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         # serializer = LikeSerializer(likes, many=True)
#         # data = list(serializer.data)
#         # return Response(data)
#         return None
