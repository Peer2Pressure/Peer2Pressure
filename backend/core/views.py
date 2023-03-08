# Built-in libraries
import json

# Third-party libraries
# from django.http import HttpResponse, JsonResponse
# from rest_framework import authentication, permission
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

# Local Libraries
from .api_serializers import *
from .serializers.authorserializer import AuthorSerializer
from .serializers.postserializer import PostSerializer
from .serializers.commentserializer import CommentSerializer
from .serializers.likeserializer import LikeSerializer
from .models import *


author_serializer = AuthorSerializer()
author_api_serializer = AuthorAPISerializer()
relation_serializer = RelationSerializer()
relation_api_serializer = RelationAPISerializer()
post_serializer = PostSerializer()
post_api_serializer = PostAPISerializer()
comment_api_serializer = CommentAPISerializer()

class CurrentAuthorID(GenericAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("USER:   ",request.user)
        author_id = request.user.author_profile.id
        return Response({'author_id': author_id})
        

class AuthorListAPI(GenericAPIView):
    serializer_class = AuthorSerializer

    def get(self, request):
        authors = author_api_serializer.get_all_authors()
        return Response(authors)
        
# class MySerializer(serializers.Serializer):
#     username = serializers.CharField()
#     email = serializers.EmailField()



class AuthorAPI(GenericAPIView):
    serializer_class = AuthorSerializer
    # swagger_schema = None
    
    def get(self, request, author_id):
        author = author_api_serializer.get_single_author(author_id)
        if author:
            return Response(author)
        return Response(data={"msg": "Author does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    # discuss if we need to change to PUT request
    # @swagger_auto_schema(request_body=MySerializer)
    def post(self, request, author_id):
        update_author = author_api_serializer.create_or_update_author(author_id, request.data)
        
        if update_author:
            return Response(update_author)
        return Response(data={"msg": "Author does not exist."}, status=status.HTTP_404_NOT_FOUND) 

class FollowerListAPI(GenericAPIView):
    serializer_class = AuthorSerializer

    def get(self, request, author_id):
        followers = relation_api_serializer.get_all_followers(author_id)
        if followers:
            return Response(followers)
        return Response(data={"msg": "Author does not exist."}, status=status.HTTP_404_NOT_FOUND)


class FollowerAPI(GenericAPIView):
    serializer_class = AuthorSerializer

    def get(self, request, author_id, foreign_author_id):
        follower = relation_api_serializer.get_single_follower(author_id, foreign_author_id)
        if follower:
            return Response(follower)
        return Response({"msg": "Follower not found"}, status=status.HTTP_404_NOT_FOUND) 
    

    def put(self, request, author_id, foreign_author_id):
        new_relation_id = relation_serializer.create_relations(author_id, foreign_author_id)
        if new_relation_id:
            new_relation = relation_serializer.get_relation_by_ids(author_id, foreign_author_id)
            return Response({"msg": f"{new_relation.from_author.username} is following {new_relation.to_author.username}"})
        return Response(data={"msg": f"Unable to follow author: {author_id}"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, author_id, foreign_author_id):
        relation = relation_api_serializer.remove_follower(author_id, foreign_author_id)
        if relation:
            return Response({"msg": "Follower has been removed successfully"})
        return Response(data={"msg": f"Unable to remover follower: {foreign_author_id}"}, status=status.HTTP_404_NOT_FOUND)


class SinglePostAPI(GenericAPIView):
    serializer_class = PostSerializer

    def get(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=author_id)
            post = Post.objects.get(pk=post_id)
        except (Author.DoesNotExist, Post.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, author_id, post_id):
        # if request.user.is_authenticated:
        #     pass
        # else:
        #     pass

        try:
            author = Author.objects.get(pk=author_id)
            is_private=request.data["is_private"]
            caption = request.data["caption"]
            image = request.data["image"]
            post = PostSerializer.create_post(author=author, is_private=is_private, id=post_id, caption=caption, image=image)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)    
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    # must be authenticated
    def post(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=author_id)
            author_id = author.id
            post = Post.objects.get(pk=post_id)
        except (Author.DoesNotExist, Post.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)    
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, author_id, post_id):
        try:
            author_id = Author.objects.get(pk=author_id)
            post = Post.objects.get(pk=post_id)
            post.delete()
        except (Author.DoesNotExist, Post.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({"msg": f"Post {post_id} has been deleted successfuly."})


class PostAPI(GenericAPIView):
    serializer_class = PostSerializer

    def get(self, request, author_id):
        posts = post_api_serializer.get_all_author_posts(author_id)
        if posts:
            return Response(posts)
        return Response(data={"msg": "Author does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, author_id):
        post_id = post_serializer.create_post(author_id, request.data)
        return Response(data={"msg": "hello world"})

class CommentAPI(GenericAPIView):
    serializer_class = CommentSerializer

    def get(self, request, author_id, post_id):
        comments = comment_api_serializer.get_post_comments(author_id, post_id)
        if comments:
            return Response(comments)
        return Response(data={"msg": "Post does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, author_id, post_id):
        comments = comment_api_serializer.add_new_comment(author_id, post_id, request.data)

        comment = request.data["comment"]
        new_comment = CommentSerializer.create_comment(author_id=author_id, post_id=post_id, comment=comment)
        if new_comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(new_comment)
        return Response(serializer.data)

class LikeAPI(GenericAPIView):
    serializer_class = LikeSerializer

    def get(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=author_id)
            post = Post.objects.get(pk=post_id)
            likes = post.likes
        except (Author.DoesNotExist, Post.DoesNotExist, Like.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LikeSerializer(likes, many=True)
        data = list(serializer.data)
        return Response(data)
    
    def post(self, request, author_id, post_id):
        comment = request.data["comment"]
        new_comment = CommentSerializer.create_comment(author_id=author_id, post_id=post_id, comment=comment)
        if new_comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(new_comment)
        return Response(serializer.data)

class LikedAPI(GenericAPIView):
    serializer_class=PostSerializer
    
    def get(self, request, author_id):
        try:
            author = Author.objects.get(pk=author_id)
            likes = author.likes
        except (Author.DoesNotExist, Like.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Like(likes, many=True)
        data = list(serializer.data)
        return Response(data)

# incomplete
class CommentLikeAPI(GenericAPIView):
    serializer_class = LikeSerializer

    def get(sef, request, author_id, post_id, comment_id):
        try:
            author = Author.objects.get(pk=author_id)
            post = Post.objects.get(pk=post_id)
            comment = Comment.objects.get(pk=comment_id)
        except (Author.DoesNotExist, Post.DoesNotExist, Comment.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        # serializer = LikeSerializer(likes, many=True)
        # data = list(serializer.data)
        # return Response(data)
        return None


class InboxLike(GenericAPIView):

    def post(self, request, author_id):
        pass

def index(request):
   if request.user.is_authenticated and not request.user.is_staff:
      return render(request, "index.html")
   else:
      return redirect('signin')

# @api_view(['POST'])
def logout_view(request):
    logout(request)
    return redirect('signin')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # CHANGE REDIRECT PAGE TO HOMEPAGE
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('/signin')

    else:
        return render(request, 'core/signin.html')
    
def signup(request):

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect("signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return redirect("signup")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_author_profile = Author.objects.create(user=user_model, first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                new_author_profile.save()
                return redirect("/signin")
        else:
            messages.info(request, "Password Not Matching")
            return redirect("/signup")
        
    else:
        return render(request, "core/signup.html")