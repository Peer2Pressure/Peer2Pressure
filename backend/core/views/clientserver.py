# Third-party libraries
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
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse

# Local Libraries
from .. import utils
from ..models import *
from ..serializers.postserializer import PostSerializer, AllPostSerializer
from ..api_serializers.post_api_serializer import PostAPISerializer

# @permission_classes([IsAuthenticated])
def get_tokens(request):
    print("hello 23")
    client_servers = ClientServer.objects.all()
    print(client_servers)
    if len(client_servers) == 0:
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
    
    response = {}

    for client in client_servers:
        response[client.host] = client.token
    print(response)
    return JsonResponse(response, status=status.HTTP_200_OK)