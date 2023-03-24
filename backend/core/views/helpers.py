from django.contrib.auth import authenticate
from base64 import b64decode

def server_request_authenticated(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2 and auth[0].lower() == 'basic':
            username, password = b64decode(auth[1]).decode('utf-8').split(':')
            server_admin = authenticate(request, username=username, password=password)
            if server_admin is not None:
                return True
    return False
