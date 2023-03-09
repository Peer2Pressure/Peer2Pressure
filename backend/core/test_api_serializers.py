# Third-party libraries
from django.test import TestCase

# Local libraries
from .models import *
from .api_serializers.author_api_serializer import AuthorAPISerializer
from .serializers.authorserializer import AuthorSerializer
from .serializers.postserializer import PostSerializer
from .serializers.relationserializer import RelationSerializer
from .serializers.likeserializer import LikeSerializer
from .serializers.commentserializer import CommentSerializer

class AuthorAPISerializerTest(TestCase):
    def setUp(self) -> None:
        self.serializer = AuthorSerializer()
        self.apiserializer = AuthorAPISerializer()

    def test_get_single_author(self):
        user = User.objects.create_user(username="authorusername", email="author@gamil.com", password="authorpassword")
        user.save()

        author_id = self.serializer.create_author("authorusername", "author firstname", "author lastname", "author@gmail.com", "authorpassword", user=user)
        self.assertTrue(author_id == self.serializer.get_author_id_by_username("authorusername"))

        author_obj = self.serializer.get_author_by_id(author_id)

        single_author_response = self.apiserializer.get_single_author(author_id)

        self.assertTrue(author_obj.id == single_author_response["id"])
        self.assertTrue("author" == single_author_response["type"])
        self.assertTrue(author_obj.username == single_author_response["username"])
        self.assertTrue(author_obj.email == single_author_response["email"])
        self.assertTrue(author_obj.first_name + " " + author_obj.last_name == single_author_response["displayName"])
        self.assertTrue(author_obj.host == single_author_response["host"])
        user.delete()

    
    def test_get_all_authors(self):
        user1 = User.objects.create_user(username="authorusername1", email="author@gamil.com", password="authorpassword")
        user1.save()

        author_id1 = self.serializer.create_author("authorusername1", "author firstname", "author lastname", "author@gmail.com", "authorpassword", user=user1)
        
        user2 = User.objects.create_user(username="authorusername2", email="author@gamil.com", password="authorpassword")
        user2.save()

        author_id2 = self.serializer.create_author("authorusername2", "author firstname1", "author lastname1", "author1@gmail.com", "authorpassword1", user=user2)

        self.assertTrue(author_id1 == self.serializer.get_author_id_by_username("authorusername1"))
        self.assertTrue(author_id2 == self.serializer.get_author_id_by_username("authorusername2"))

        first_author_obj = self.serializer.get_author_by_id(author_id1)
        second_author_obj = self.serializer.get_author_by_id(author_id2)

        all_authors_response = self.apiserializer.get_all_authors()

        self.assertTrue("authors" == all_authors_response["type"])
        self.assertTrue(2 == len(all_authors_response["items"]))
        self.assertTrue(first_author_obj.username == all_authors_response["items"][0]["username"])
        self.assertTrue(first_author_obj.id == all_authors_response["items"][0]["id"])
        self.assertTrue(first_author_obj.email == all_authors_response["items"][0]["email"])
        self.assertTrue(first_author_obj.first_name + " " + first_author_obj.last_name == all_authors_response["items"][0]["displayName"])
        self.assertTrue(first_author_obj.host == all_authors_response["items"][0]["host"])
        self.assertTrue(second_author_obj.username == all_authors_response["items"][1]["username"])
        self.assertTrue(second_author_obj.id == all_authors_response["items"][1]["id"])
        self.assertTrue(second_author_obj.email == all_authors_response["items"][1]["email"])
        self.assertTrue(second_author_obj.first_name + " " + second_author_obj.last_name == all_authors_response["items"][1]["displayName"])
        self.assertTrue(second_author_obj.host == all_authors_response["items"][1]["host"])

        user1.delete()
        user2.delete()


    # def test_author_create(self):
        # author_id = self.serializer.create_author("author username", "author firstname", "author lastname", "author@gmail.com", "authorpassword")
    #     result_dict = self.apiserializer.get_single_author(author_id)

    #     self.assertTrue(result_dict["type"] == "author")
    #     self.assertTrue(result_dict["displayName"] == "author username")
    #     self.assertTrue(result_dict["github"] == "author@gmail.com")

    #     print(result_dict)

    # def test_get_all_authors(self):
    #     author_id1 = self.serializer.create_author("author username", "author firstname", "author lastname", "author@gmail.com", "authorpassword")
    #     result_dict = self.apiserializer.get_all_authors()

    #     print(result_dict)