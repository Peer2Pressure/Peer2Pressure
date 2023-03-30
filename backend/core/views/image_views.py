# Built-in libraries
import json

# Third-party libraries
from django.http import HttpResponse, JsonResponse
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
from ..api_serializers.image_api_handler import PostImageHandler


image_handler = PostImageHandler()

class PostImageAPI(GenericAPIView):
    # serializer_class = AllFollowerSerializer
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Followers"],
        operation_description="Get a list of all followers for an author"
    )
    def get(self, request, author_id, post_id):
        image, code = image_handler.get_image_from_base64(author_id, post_id)
        if code == 200:
            return HttpResponse(image, status=status.HTTP_200_OK)
        elif code == 400:
            return Response(image, status=status.HTTP_400_BAD_REQUEST)
        elif code == 404:
            return Response(image, status=status.HTTP_404_NOT_FOUND)
