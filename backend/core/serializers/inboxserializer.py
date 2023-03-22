# Built-in libraries
import base64
from uuid import uuid4

# Third-party libraries
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from varname import nameof        

# Local libraries
from .. models import *
from ..serializers.postserializer import PostSerializer
from django.core.files.base import ContentFile

class InboxItemsSerializer(serializers.Serializer):
    type = serializers.CharField(default="inbox" , max_length=10, read_only=True, required=False)
    page = serializers.IntegerField(allow_null=True, required=False)
    size = serializers.IntegerField(allow_null=True, required=False)
    items = PostSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['page'] is None:
            data.pop('page')
        if data['size'] is None:
            data.pop('size')
        return data