# Built-in libraries
import json
import time
import uuid


# Third-party libraries
# from django.http import HttpResponse, JsonResponse
# from rest_framework import authentication, permission
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.utils import timezone
from django.contrib.auth import logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.middleware.csrf import rotate_token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import permission_classes
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder

# Local Libraries
from .. import utils
from ..models import *
from ..serializers.authorserializer import AuthorSerializer
from ..serializers.postserializer import PostSerializer
from ..api_serializers.post_api_serializer import PostAPISerializer
from ..api_serializers.inbox_api_serializer import InboxAPISerializer

author_serializer = AuthorSerializer()

import pprint

pp = pprint.PrettyPrinter(indent=0)

class InboxStreamView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, author_id):
        response = StreamingHttpResponse(self.stream_events(request, author_id), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        # response['Connection'] = 'keep-alive'
        response["Access-Control-Allow-Origin"] = '*'
        return response
        
    def stream_events(self, request, author_id):
        try:
            author = author_serializer.get_author_by_id(author_id)

            # Get all posts from the author's inbox
            inbox = author.inbox.all().filter(type="post").order_by('-created_at')
            last_created_at = inbox[0].created_at

            inbox_posts = [inbox_obj.content_object for inbox_obj in inbox if inbox_obj.content_object.unlisted == False]
            print(inbox_posts)

            # # Create a new response object for each client connection
            # response = StreamingHttpResponse(content_type='text/event-stream')

            new_messages = PostSerializer(inbox_posts, many=True).data
            
            # new_messages = json.dumps(messages, cls=DjangoJSONEncoder)
            for message in new_messages:
                json_string_msg = json.dumps(messages, cls=DjangoJSONEncoder)
                yield "data: {}\n\n".format(json_string_msg)


            yield "data: {}\n\n".format(message)
            print("-----------------------------------")
            # Continuously stream new inbox messages to the client
            while True:
                new_inbox = Inbox.objects.filter(author=author, type="post", created_at__gt=last_created_at).order_by('-created_at')
                print("new inbo123: ", new_inbox, len(new_inbox))

                if len(new_inbox) != 0:
                    last_created_at = new_inbox[0].created_at
                
                    new_inbox_posts = [inbox_obj.content_object for inbox_obj in new_inbox if inbox_obj.content_object.unlisted == False]
                    new_messages = PostSerializer(new_inbox_posts, many=True).data
                    
                    print("new messages", new_messages)
                    # push_message(new_messages)

                    # print(new_messages)
                    for message in new_messages:
                        json_string_msg = json.dumps(message, cls=DjangoJSONEncoder)
                        yield "data: {}\n\n".format(json_string_msg)

                # Sleep for a short time to prevent high CPU usage
                
                time.sleep(1)

        except Author.DoesNotExist:
            print("Author does not exist.")