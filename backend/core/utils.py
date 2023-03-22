import re
from uuid import UUID
from urllib.parse import urlparse
from rest_framework.exceptions import ValidationError

def get_pagination_variables(query_params):
    if len(query_params) == 0:
        return None, None
    
    page = query_params.get("page")
    size = query_params.get("size")

    try:
        page = int(page)
        size = int(size)
    except (TypeError, ValueError):
        raise ValidationError("Invalid page or size values.")
    
    if page < 1 or size < 1:
        raise ValidationError("Page and size paramteres must be a positive integer.")

    return page, size

def paginate_list(orig_list, page, size):
    start = (page - 1) * size
    stop = page * size

    return orig_list[start:stop]



def validate_followers_url_path(value):
    """
    Validates that a string is a valid URL and its path matches the pattern '/authors/<uuid>/followers/<uuid>/'.
    """
    url = urlparse(value)
    
    # Check if the string is a valid URL
    if not all([url.scheme, url.netloc]):
        raise ValidationError('Invalid URL format.')
    
    # Check if the path matches the expected format
    path_pattern = r'^/authors/(?P<author_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/followers/(?P<follower_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$'
    path_regex = re.compile(path_pattern)
    match = path_regex.match(url.path)
    
    if not match:
        raise ValidationError('Invalid URL path. The path should match the pattern: /authors/<uuid>/followers/<uuid>/')
    
    author_uuid_str = match.group('author_uuid')
    follower_uuid_str = match.group('follower_uuid')
    
    try:
        UUID(author_uuid_str)
        UUID(follower_uuid_str)
    except ValueError:
        raise ValidationError('Invalid UUID format. UUID should be in the standard format.')
    