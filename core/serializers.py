from rest_framework import serializers
from . models import *
from varname import nameof

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def create_author(self, username, firstname, lastname, email, password, host = None):

        if host is not None:
            defaults = {
                nameof(Author.host): host,
                nameof(Author.username): username,
                nameof(Author.first_name): firstname,
                nameof(Author.last_name): lastname,
                nameof(Author.email): email,
                nameof(Author.password): password
            }
        else:
            defaults = {
                nameof(Author.username): username,
                nameof(Author.first_name): firstname,
                nameof(Author.last_name): lastname,
                nameof(Author.email): email,
                nameof(Author.password): password
            }

        author_obj= Author.objects.create(**defaults)

        return author_obj.id

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

class RelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relations
        fields = "__all__"

    def create_relations(self, from_author, to_author):

        try:
            from_author_obj = Author.objects.get(id=from_author)
        except Author.DoesNotExist:
            raise ValueError("From Author does not exist")
        
        try:
            to_author_obj = Author.objects.get(id=to_author)
        except Author.DoesNotExist:
            raise ValueError("To Author does not exist")
        
        defaults = {
            nameof(Relations.from_author): from_author_obj,
            nameof(Relations.to_author): to_author_obj
        }

        relation_obj= Relations.objects.create(**defaults)

        return relation_obj.id

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"

    def create_like(self, like_author, post):

        try:
            like_author_obj = Author.objects.get(id=like_author)
        except Author.DoesNotExist:
            raise ValueError("Like Author does not exist")
        
        try:
            post_obj = Post.objects.get(id=post)
        except Post.DoesNotExist:
            raise ValueError("Post does not exist")
        
        defaults = {
            nameof(Like.like_author): like_author_obj,
            nameof(Like.post): post_obj
        }

        like_obj = Like.objects.create(**defaults)

        return like_obj.id

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
    
    def create_comment(self, comment_author, post, comment):

        try:
            comment_author_obj = Author.objects.get(id=comment_author)
        except Author.DoesNotExist:
            raise ValueError("Comment Author does not exist")
        
        try:
            post_obj = Post.objects.get(id = post)
        except Post.DoesNotExist:
            raise ValueError("Post does not exist")
        
        defaults = {
            nameof(Comment.comment_author): comment_author_obj,
            nameof(Comment.post): post_obj,
            nameof(comment): comment
        }

        comment_obj, comment_created = Comment.objects.create(defaults=defaults)

        return comment_obj.id, comment_created        