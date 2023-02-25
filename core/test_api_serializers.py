from .models import *
from django.test import TestCase
from .serializers import *
from .api_serializers import *

class AuthorAPISerializerTest(TestCase):
    def setUp(self) -> None:
        self.serializer = AuthorSerializer()
        self.apiserializer = AuthorAPISerializer()

    def test_author_create(self):
        author_id = self.serializer.create_author("author username", "author firstname", "author lastname", "author@gamil.com", "authorpassword")
        result_dict = self.apiserializer.get_single_author(author_id)

        self.assertTrue(result_dict["type"] == "author")
        self.assertTrue(result_dict["displayName"] == "author username")
        self.assertTrue(result_dict["github"] == "author@gmail.com")

        print(result_dict)