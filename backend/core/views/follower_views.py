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
from ..serializers.relationserializer import RelationSerializer
from ..api_serializers.relation_api_serializer import RelationAPISerializer

relation_serializer = RelationSerializer()
relation_api_serializer = RelationAPISerializer()

class FollowerListAPI(GenericAPIView):
    serializer_class = AuthorSerializer

    def get(self, request, author_id):
        followers = relation_api_serializer.get_all_followers(author_id)
        if followers:
            return Response(followers)
        return Response(data={"msg": "Author does not exist."}, status=status.HTTP_404_NOT_FOUND)


class FollowerAPI(GenericAPIView):
    serializer_class = AuthorSerializer

    def get(self, request, author_id, foreign_author_id):
        follower = relation_api_serializer.get_single_follower(author_id, foreign_author_id)
        if follower:
            return Response(follower)
        return Response({"msg": "Follower not found"}, status=status.HTTP_404_NOT_FOUND) 
    

    def put(self, request, author_id, foreign_author_id):
        new_relation_id = relation_serializer.create_relations(author_id, foreign_author_id)
        if new_relation_id:
            new_relation = relation_serializer.get_relation_by_ids(author_id, foreign_author_id)
            return Response({"msg": f"{new_relation.from_author.username} is following {new_relation.to_author.username}"})
        return Response(data={"msg": f"Unable to follow author: {author_id}"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, author_id, foreign_author_id):
        relation = relation_api_serializer.remove_follower(author_id, foreign_author_id)
        if relation:
            return Response({"msg": "Follower has been removed successfully"})
        return Response(data={"msg": f"Unable to remover follower: {foreign_author_id}"}, status=status.HTTP_404_NOT_FOUND)
