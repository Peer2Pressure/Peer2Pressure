# Built-in libraries
import base64

# Local libraries
from .. import utils
from ..models import *
from ..serializers.authorserializer import AuthorSerializer, AllAuthorSerializer
from ..serializers.postserializer import PostSerializer
from ..config import *

post_serializer = PostSerializer()

class PostImageHandler():
    def get_image_from_base64(self, author_id, post_id):
        if not post_serializer.post_exists(author_id, post_id):
            print("aaaaaaaaaaaa")
            return "", 404

        valid_image_content_types = ["image/png;base64", "image/jpeg;base64"]
        post = post_serializer.get_author_post(author_id, post_id)

        if post.content_type not in valid_image_content_types:
            print("bbbbbbbbbbbb")
            return "", 404
        

        img_data = post.content.split(',')[1]
        img_bytes = base64.b64decode(img_data)
        print(img_bytes)
        
        return img_bytes, 200