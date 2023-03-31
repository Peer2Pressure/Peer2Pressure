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
from ..models import *


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
            return redirect('signin')
    else:
        return render(request, 'core/signin.html')
    
def signup(request):

    if request.method == "POST":
        name = request.POST["name"]
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
                user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
                user.save()

                user_model = User.objects.get(username=username)

                new_author_profile = Author.objects.create(user=user_model, name=name, username=username, email=email, password=password, avatar="", github="")
                new_author_profile.save()
                return redirect("signin")
        else:
            messages.info(request, "Password Not Matching")
            return redirect("signup")
        
    else:
        return render(request, "core/signup.html")