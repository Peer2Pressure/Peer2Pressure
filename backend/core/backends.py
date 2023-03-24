from django.contrib.auth.backends import BaseBackend
from models import ServerAdmin
from django.contrib.auth.hashers import check_password

class BasicAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            server_admin = ServerAdmin.objects.get(username=username)
            if server_admin.check_password(password):
                return server_admin
        except ServerAdmin.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return ServerAdmin.objects.get(pk=user_id)
        except ServerAdmin.DoesNotExist:
            return None