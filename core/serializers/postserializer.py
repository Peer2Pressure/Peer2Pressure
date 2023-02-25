# Local libraries
from .. models import *

# Third-party libraries
from rest_framework import serializers
from varname import nameof        

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def create_post(self, author, is_private, image = None, caption = None):

        if image is None and caption is None:
            raise ValueError("Require eithr caption or image for the post")

        try:
            author_obj = Author.objects.get(id=author)
        except Author.DoesNotExist:
            raise ValueError("Author does not exist")

        defaults = {
            nameof(Post.author): author_obj,
            nameof(Post.is_private): is_private
        }

        if image is not None:
            defaults[nameof(Post.image)] = image

        if caption is not None:
            defaults[nameof(Post.caption)] = caption

        post_obj = Post.objects.create(**defaults)

        return post_obj.id
