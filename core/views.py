# Built-in libraries
import json

# Third-party libraries
# from django.http import HttpResponse, JsonResponse
# from rest_framework import authentication, permission
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

# Local Libraries
from .api_serializers import AuthorAPISerializer
from .serializers.authorserializer import AuthorSerializer
from .models import Author, Relation


authorapi_serializer = AuthorAPISerializer()

class AuthorListAPI(GenericAPIView):
    serializer_class = AuthorSerializer

    def get(self, request):
        authors = Author.objects.all()    
        serializer = AuthorSerializer(authors, many=True)
        data = list(serializer.data)
        return Response(data)

class AuthorAPI(GenericAPIView):
    serializer_class = AuthorAPISerializer
    def get(self, request, author_id):
        author = authorapi_serializer.get_single_author(author_id)
        return Response(author)
    
    # discuss if we need to change to PUT request
    def post(self, request, author_id):
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)    
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class FollowerListAPI(GenericAPIView):
    serializer_class = AuthorAPISerializer

    def get(self, request, author_id):
        try:
            following_ids = list(Author.objects.get(pk=author_id).follower.all().values_list('from_author', flat=True))

            # Uncomment if using bool to set relations
            # followers = list(Relation.objects.filter(from_author=author_id, to_author_request=True).values_list('to_author', flat=True))
            # followers += list(Relation.objects.filter(to_author=author_id, from_author_request=True).values_list('from_author', flat=True))

            authors = Author.objects.filter(pk__in=following_ids)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

class FollowerAPI(GenericAPIView):
    serializer_class = AuthorAPISerializer

    def delete(self, request, author_id, foreign_author_id):
        try:
            follower = Relation.objects.get(from_author=foreign_author_id, to_author=author_id)
            follower_author = follower.from_author
            follower.delete()
        except Relation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # serializer = AuthorSerializer(follower_author.from_author)
        return Response({"msg": f"{follower_author.username} has been removed from as a follower."})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # CHANGE REDIRECT PAGE TO HOMEPAGE
            return redirect('/swagger')
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