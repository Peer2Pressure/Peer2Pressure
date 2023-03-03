# Local libraries
from .. models import *

# Third-party libraries
from rest_framework import serializers
from varname import nameof        

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def create_post(self, author, is_private, post_id=None, image=None, caption=None):

        if image is None and caption is None:
            print("Require either caption or image for the post")
            return None
            # raise ValueError("Require either caption or image for the post")

        try:
            author_obj = Author.objects.get(id=author)
        except Author.DoesNotExist:
            print("Author does not exist")
            return None
            # raise ValueError("Author does not exist")

        defaults = {
            
            nameof(Post.author): author_obj,
            nameof(Post.is_private): is_private
        }

        if post_id is not None:
            defaults[nameof(Post.id)] = post_id
        if image is not None:
            defaults[nameof(Post.image)] = image
        if caption is not None:
            defaults[nameof(Post.caption)] = caption

        post_obj = Post.objects.create(**defaults)

        return post_obj

    def get_post(self, authorid, postid):

        try:
            post_obj = Post.objects.get(author_id=authorid, id = postid)
        except Post.DoesNotExist:
            return None

        return post_obj