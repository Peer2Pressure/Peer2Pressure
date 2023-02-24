from rest_framework import serializers
from . models import *
from varname import nameof

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def create_author(self, username, firstname, lastname, email, password):

        identifiers = {
            nameof(Author.username): username
        }

        defaults = {
            nameof(Author.first_name): firstname,
            nameof(Author.last_name): lastname,
            nameof(Author.email): email,
            nameof(Author.password): password
        }

        author_obj, author_created = Author.objects.update_or_create(**identifiers, defaults=defaults)

        return author_obj.id, author_created

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def create_post(self, author, image, caption, is_private):

        try:
            author_obj = Author.objects.get(username=author)
        except Author.DoesNotExist:
            raise ValueError("Author does not exist")
        
        defaults = {
            nameof(Post.author): author_obj,
            nameof(Post.image): image,
            nameof(Post.caption): caption,
            nameof(Post.is_private): is_private
        }

        post_obj, post_created = Post.objects.create(defaults=defaults)

        return post_obj, post_created

class RelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relations
        fields = "__all__"

    def create_relations(self, from_author, to_author):

        try:
            from_author_obj = Author.objects.get(username=from_author)
        except Author.DoesNotExist:
            raise ValueError("From Author does not exist")
        
        try:
            to_author_obj = Author.objects.get(username=to_author)
        except Author.DoesNotExist:
            raise ValueError("To Author does not exist")
        
        defaults = {
            nameof(Relations.from_author): from_author_obj,
            nameof(Relations.to_author): to_author_obj
        }

        relation_obj, relation_created = Relations.objects.create(defaults=defaults)

        return relation_obj, relation_created

# class LikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Like
#         fields = "__all__"

#     def create_like(self, like_author, post):

        