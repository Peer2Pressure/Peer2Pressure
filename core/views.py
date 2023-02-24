from .serializers import AuthorSerializer
from .models import Author

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

# Create your views here.
def index(request):
    return render(request, "index.html")

@api_view(['GET'])
def author_list(request):
    '''
    Gets all authors
    '''
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return JsonResponse(serializer.data, safe=False)


