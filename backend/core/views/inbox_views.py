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
from django.middleware.csrf import rotate_token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import permission_classes
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.decorators import login_required
from urllib.parse import urlparse


# Local Libraries
from .. import utils
from ..models import *
from ..serializers.postserializer import PostSerializer
from ..api_serializers.post_api_serializer import PostAPISerializer
from ..api_serializers.inbox_api_serializer import InboxAPISerializer

# API serializer
inbox_api_serializer = InboxAPISerializer()

# def redirect_to_inbox(request):
#     rotate_token(request)
#     return redirect('inbox', permanent=True)

class InboxAPI(GenericAPIView):
    serializer_class = PostSerializer

    @swagger_auto_schema(
        tags=["Inbox"],
        operation_description="Get all posts from author's inbox.",
    )
    def get(self, request, author_id):
        try:
            page, size = utils.get_pagination_variables(request.query_params)
        except ValidationError:
            return Response(data={"msg": "Invalid query parameters."}, status=status.HTTP_400_BAD_REQUEST)

        data_type = request.query_params.get("type", "post")
        
        response, code = inbox_api_serializer.get_all_inbox_posts(author_id, page=page, size=size, data_type=data_type)
        if code == 200:
            return Response(response, status=status.HTTP_200_OK)
        elif code == 400:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        elif code == 404:
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        return Response(data={"msg": "Unable to get inbox posts."}, status=status.HTTP_404_NOT_FOUND)

    # TODO: Only if user is authenticated
    @swagger_auto_schema(
        tags=["Inbox"],
        operation_description="Send an object to an author's obj",
    )
    @permission_classes([IsAuthenticated])
    def post(self, request, author_id):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')    

        response = None
        code = None
        if "type" in list(request.data.keys()):
            if request.data["type"].lower() == "post":
                response, code = inbox_api_serializer.handle_post(author_id, request.data, auth_header)
            elif request.data["type"].lower() == "follow":
                response, code = inbox_api_serializer.handle_follow_request(author_id, request.data)
            elif request.data["type"].lower() == "like":
                post_or_comment = urlparse(request.data["object"]).path.split('/')[-2]
                if post_or_comment == "posts":    
                    response, code = inbox_api_serializer.handle_like_request(author_id, request.data)
                elif post_or_comment == "comments":
                    response, code = inbox_api_serializer.handle_comment_like_request(author_id, request.data)
            elif request.data["type"].lower() == "comment":
                print("COMMENT REQUEST: ", request.data)
                response, code = inbox_api_serializer.handle_comment_request(author_id, request.data)
        if code == 200:
            return Response(response, status=status.HTTP_200_OK)
        elif code == 400:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        elif code == 404:
            return Response(response, status=status.HTTP_404_NOT_FOUND)