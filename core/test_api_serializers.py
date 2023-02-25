from .models import *
from django.test import TestCase
from .api_serializers import *
from .serializers.authorserializer import AuthorSerializer
from .serializers.postserializer import PostSerializer
from .serializers.relationserializer import RelationSerializer
from .serializers.likeserializer import LikeSerializer
from .serializers.commentserializer import CommentSerializer

class AuthorAPISerializerTest(TestCase):
    def setUp(self) -> None:
        self.serializer = AuthorSerializer()
        self.apiserializer = AuthorAPISerializer()

    def test_author_create(self):
        author_id = self.serializer.create_author("author username", "author firstname", "author lastname", "author@gmail.com", "authorpassword")
        result_dict = self.apiserializer.get_single_author(author_id)

        self.assertTrue(result_dict["type"] == "author")
        self.assertTrue(result_dict["displayName"] == "author username")
        self.assertTrue(result_dict["github"] == "author@gmail.com")

        print(result_dict)