from django.urls import is_valid_path
from django.shortcuts import redirect

class AddTrailingSlashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Check if the path is valid and does not end with a trailing slash
        if not is_valid_path(request.path_info) and not request.path_info.endswith('/'):
            # Add a trailing slash to the path
            new_url = request.path_info + '/'
            # Redirect to the new URL
            return redirect(new_url, permanent=True)
        
        response = self.get_response(request)
        return response