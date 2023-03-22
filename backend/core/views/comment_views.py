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
from ..api_serializers.comment_api_serializer import CommentAPISerializer
from ..serializers.commentserializer import CommentSerializer
from ..models import *

# API serializer
comment_api_serializer = CommentAPISerializer()


class CommentAPI(GenericAPIView):
    serializer_class = CommentSerializer

    @swagger_auto_schema(tags=['Comments'])
    def get(self, request, author_id, post_id):
        try:
            page, size = utils.get_pagination_variables(request.query_params)
        except ValidationError:
            return Response(data={"msg": "Invalid query parameters."}, status=status.HTTP_400_BAD_REQUEST)

        comments = comment_api_serializer.get_post_comments(author_id, post_id, page, size)
        if comments:
            return Response(comments)
        return Response(data={"msg": "Post does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(tags=['Comments'])
    def post(self, request, author_id, post_id):
        new_comment = comment_api_serializer.add_new_comment(author_id, post_id, request.data)
        if new_comment is None:
            return Response(data={"msg": "Unable comment on post"}, status=status.HTTP_404_NOT_FOUND)
        return Response(new_comment)
