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
from ..serializers.authorserializer import AuthorSerializer
from ..serializers.followerserializer import FollowerSerializer, AllFollowerSerializer
from ..api_serializers.follower_api_serializer import FollowerAPISerializer

follower_serializer = FollowerSerializer()
follower_api_serializer = FollowerAPISerializer()

class FollowerListAPI(GenericAPIView):
    serializer_class = AllFollowerSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Followers"],
        operation_description="Get a list of all followers for an author"
    )
    def get(self, request, author_id):
        followers, code = follower_api_serializer.get_all_followers(author_id)
        if code == 200:
            return Response(followers, status=status.HTTP_200_OK)
        elif code == 400:
            return Response(followers, status=status.HTTP_400_BAD_REQUEST)
        elif code == 404:
            return Response(followers, status=status.HTTP_404_NOT_FOUND)


class FollowerAPI(GenericAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Followers'])
    def get(self, request, author_id, foreign_author_id):        
        follower, code = follower_api_serializer.get_single_follower(author_id, foreign_author_id)
        if code == 200:
            return Response(follower, status=status.HTTP_200_OK)
        elif code == 404:
            return Response(follower, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=['Followers'])
    def put(self, request, author_id, foreign_author_id):
        response, code = follower_api_serializer.create_follow_request(author_id, foreign_author_id, request.data)
        if code == 200:
            return Response(response, status=status.HTTP_200_OK)
        elif code == 400:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        elif code == 404:
            return Response(response, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(tags=['Followers'])
    def delete(self, request, author_id, foreign_author_id):
        follower, code = follower_api_serializer.remove_follower(author_id, foreign_author_id)
        if code == 200:
            return Response(follower, status=status.HTTP_200_OK)
        elif code == 404:
            return Response(follower, status=status.HTTP_404_NOT_FOUND)
