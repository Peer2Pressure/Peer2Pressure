from rest_framework import serializers
from . models import *
from varname import nameof

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def create_author(self, username, firstname, lastname, email, password):

        defaults = {
            nameof(Author.username): username,
            nameof(Author.first_name): firstname,
            nameof(Author.last_name): lastname,
            nameof(Author.email): email,
            nameof(Author.password): password
        }

        author_obj, author_created = Author.objects.create(defaults=defaults)

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

        return post_obj.id, post_created

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

        relation_obj, relation_created = Relations.objects.create(defaults=defaults)

        return relation_obj.id, relation_created

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

        like_obj, like_created = Like.objects.create(defaults=defaults)

        return like_obj.id, like_created

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