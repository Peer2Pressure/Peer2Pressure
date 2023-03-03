# Third-party libraries
from rest_framework import serializers
from varname import nameof        

# Local libraries
from .. models import *
from ..serializers.authorserializer import AuthorSerializer

author_serializer = AuthorSerializer()

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {'image': {'required': False, 'allow_null': True}}

    def create_post(self, author_id, request_data):
        field_names = [field.name for field in Post._meta.get_fields()]

        if "image" not in list(request_data.keys()) and "content" not in list(request_data.keys()):
            print("Require either contetn or image for the post")
            return None
            # raise ValueError("Require either caption or image for the post")

        try:
            author = author_serializer.get_author_by_id(author_id)
        except ValueError:
            print("Author does not exist")
            return None
            # raise ValueError("Author does not exist")

        defaults = {
            nameof(Post.author): author,
        }

        for key in request_data:
            if key in field_names:
                defaults[key] = request_data[key]

        post = Post.objects.create(**defaults)

        return post.id




