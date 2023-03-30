from urllib.parse import urlparse

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
    client_servers = Node.objects.all()
    if len(client_servers) == 0:
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
    
    response = {}

    for client in client_servers:
        hostname = urlparse(client.api_endpoint).hostname
        response[hostname] = client.token
    return JsonResponse(response, status=status.HTTP_200_OK)

def get_api_endpoints(request):
    client_servers = Node.objects.all()
    if len(client_servers) == 0:
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
    
    response = {
        "type": "api_endpoints",
        "items": []
    }

    for client in client_servers:
        response["items"].append(client.api_endpoint)

    return JsonResponse(response, status=status.HTTP_200_OK)

def get_hostnames(request):
    client_servers = Node.objects.all()
    if len(client_servers) == 0:
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
    
    response = {
        "type": "hostnames",
        "items": []
    }

    for client in client_servers:
        hostname = urlparse(client.host).hostname
        response["items"].append(hostname)

    return JsonResponse(response, status=status.HTTP_200_OK)
