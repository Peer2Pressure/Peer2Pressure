# Local libraries
from ..models import *

# Third-party libraries
from rest_framework import serializers
from varname import nameof
from .authorserializer import AuthorSerializer
from .commentserializer import CommentSerializer

class CommentLikeSerializer(serializers.ModelSerializer):
    summary = serializers.CharField(required=False)
    type = serializers.CharField(required=False, max_length=10, default="like", read_only=True)
    author = AuthorSerializer(required=True)
    object = serializers.URLField(required=True)

    class Meta:
        model = CommentLike
        fields = ["summary", "type", "author", "object"]
