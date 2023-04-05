# Built-in libraries
import json
import time
import uuid
import socket

# Third-party libraries
from django.http import StreamingHttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder

from django.core.signals import request_finished
from django.dispatch import receiver

# Local Libraries
from .. import utils
from ..models import *
from ..serializers.authorserializer import AuthorSerializer
from ..serializers.postserializer import PostSerializer


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
        
        if response.streaming_content:
            try:
                for chunk in response.streaming_content:
                    # Attempt to write the chunk to the client
                    # This will raise an IOError if the client has disconnected
                    response.write(chunk)
            except IOError:
                # Handle client disconnect here
                print("ERROR while wrting chunk ====")    

        # print()
        # print(response.streaming_content)
        # print("123 send", response.closed)
        # print()

        return response
        
    def stream_events(self, request, author_id):
        yield "@" * 50 * 1024

        try:
            author = author_serializer.get_author_by_id(author_id)

            # Get all posts from the author's inbox
            inbox = author.inbox.all().filter(type="post").order_by('-created_at')
            last_created_at = inbox[0].created_at

            inbox_posts = [inbox_obj.content_object for inbox_obj in inbox if inbox_obj.content_object.unlisted == False]

            new_messages = PostSerializer(inbox_posts, many=True).data

            # Sleeping 10 seconds to allow client to setup connection
            print("Sleeping 10 seconds to allow client to setup connection\n")
            time.sleep(10)

            for message in new_messages:
                json_string_msg = json.dumps(message, cls=DjangoJSONEncoder)
                yield "data: {}\n\n".format(json_string_msg)

            print("-----------------------------------")

            # Continuously stream new inbox messages to the client
            counter = 1
            while True:
                from django.core.handlers.wsgi import LimitedStream
                # limited_stream = request.META.get('wsgi.input')
                # print(limited_stream)
                # print("=====", limited_stream.stream, limited_stream.buffer, limited_stream.remaining)
                
                new_inbox = Inbox.objects.filter(author=author, type="post", created_at__gt=last_created_at).order_by('-created_at')
                print("new inbo123: ", new_inbox, len(new_inbox))

                if len(new_inbox) != 0:
                    last_created_at = new_inbox[0].created_at
                
                    new_inbox_posts = [inbox_obj.content_object for inbox_obj in new_inbox if inbox_obj.content_object.unlisted == False]
                    new_messages = PostSerializer(new_inbox_posts, many=True).data
                    
                    print("new messages", new_messages)

                    for message in new_messages:
                        json_string_msg = json.dumps(message, cls=DjangoJSONEncoder)
                        yield "data: {}\n\n".format(json_string_msg)

                # Sleep for a short time to prevent high CPU usage                
                time.sleep(1)

                if counter % 10 == 0:
                    print("TESTING CONNECTION IS STILL OPEN")
                    yield "data: {}\n\n".format('{}')
                    counter = 1
                    
                
                counter += 1
                print(counter)

        except Author.DoesNotExist:
            print("Author does not exist.")
        
                    
        print("CONNECTION CLOSED....")