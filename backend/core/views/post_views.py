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
from ..models import *
from ..serializers.postserializer import PostSerializer
from ..api_serializers.post_api_serializer import PostAPISerializer

# API serializer
post_api_serializer = PostAPISerializer()

class SinglePostAPI(GenericAPIView):
    serializer_class = PostSerializer

    def get(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=author_id)
            post = Post.objects.get(pk=post_id)
        except (Author.DoesNotExist, Post.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, author_id, post_id):
        # if request.user.is_authenticated:
        #     pass
        # else:
        #     pass

        try:
            author = Author.objects.get(pk=author_id)
            is_private=request.data["is_private"]
            caption = request.data["caption"]
            image = request.data["image"]
            post = PostSerializer.create_post(author=author, is_private=is_private, id=post_id, caption=caption, image=image)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)    
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    # must be authenticated
    def post(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=author_id)
            author_id = author.id
            post = Post.objects.get(pk=post_id)
        except (Author.DoesNotExist, Post.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)    
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, author_id, post_id):
        try:
            author_id = Author.objects.get(pk=author_id)
            post = Post.objects.get(pk=post_id)
            post.delete()
        except (Author.DoesNotExist, Post.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({"msg": f"Post {post_id} has been deleted successfuly."})


class PostAPI(GenericAPIView):
    serializer_class = PostSerializer

    def get(self, request, author_id):
        posts = post_api_serializer.get_all_author_posts(author_id)
        if posts:
            return Response(posts)
        return Response(data={"msg": "Author does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, author_id):
        post = post_api_serializer.add_new_post(author_id, request.data)
        if post:
            return Response(post)
        return Response(data={"msg": "Unable to create post"}, status=status.HTTP_404_NOT_FOUND)
