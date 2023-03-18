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