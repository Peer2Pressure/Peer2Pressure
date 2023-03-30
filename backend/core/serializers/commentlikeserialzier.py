# Local libraries
from ..models import *

# Third-party libraries
from rest_framework import serializers
from varname import nameof
from .authorserializer import AuthorSerializer

class CommentLikeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(required=False, max_length=10, default="like", read_only=True)
    summary = serializers.CharField(required=False)
    author = AuthorSerializer(required=True)
    object = serializers.URLField(required=True)

    class Meta:
        model = PostLike
        fields = ["type", "summary", "author", "object"]
