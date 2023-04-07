# Third-party libraries
from django.test import TestCase

# Local libraries
from .models import *
from .api_serializers.author_api_serializer import AuthorAPISerializer
from .api_serializers.follower_api_serializer import FollowerAPISerializer
from .serializers.authorserializer import AuthorSerializer
from .serializers.postserializer import PostSerializer
from .serializers.followerserializer import FollowerSerializer
from .serializers.postlikeserializer import PostLikeSerializer
from .serializers.commentserializer import CommentSerializer

class AuthorAPISerializerTest(TestCase):
    def setUp(self) -> None:
        self.serializer = AuthorSerializer()
        self.apiserializer = AuthorAPISerializer()

    def test_get_single_author(self):
        user = Author.objects.create(
            name="John Doe",
            username="johndoe",
            email="johndoe@example.com",
            password="password",
            github="https://github.com/johndoe",
            avatar=""
        )
    
        self.assertTrue(user.id == self.serializer.get_author_id_by_username("johndoe"))

        author_obj = self.serializer.get_author_by_id(user.m_id)

        single_author_response = self.apiserializer.get_single_author(user.m_id)

        self.assertTrue(author_obj.id == single_author_response["id"])
        self.assertTrue("author" == single_author_response["type"])
        self.assertTrue(author_obj.id == single_author_response["url"])
        self.assertTrue(author_obj.name == single_author_response["displayName"])
        self.assertTrue(author_obj.github == single_author_response["github"])
    
    def test_get_all_authors(self):

        all_authors_response = self.apiserializer.get_all_authors()
        print(all_authors_response)
        self.assertTrue("authors" == all_authors_response[0]["type"])
        self.assertTrue(0 == len(all_authors_response[0]["items"]))
        user = Author.objects.create(
            name="John Doe",
            username="johndoe",
            email="johndoe@example.com",
            password="password",
            github="https://github.com/johndoe",
            avatar=""
        )
        all_authors_response = self.apiserializer.get_all_authors()
        print(all_authors_response)
        self.assertTrue("authors" == all_authors_response[0]["type"])
        self.assertTrue(1 == len(all_authors_response[0]["items"]))
        self.assertTrue(user.id == all_authors_response[0]["items"][0]["id"])
        self.assertTrue(user.name == all_authors_response[0]["items"][0]["displayName"])
        self.assertTrue(user.github == all_authors_response[0]["items"][0]["github"])

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

# class RelationAPISerializerTest(TestCase):
#     def setUp(self) -> None:
#         self.authorserializer = AuthorSerializer()
#         self.authorapiserializer = AuthorAPISerializer()
#         self.user_1 = User.objects.create_user(username="authorusername1", email="author@gamil.com", password="authorpassword")
#         self.user_1.save()
#         self.author_id1 = self.authorserializer.create_author("authorusername1", "author firstname", "author lastname", "author@gamil.com", "authorpassword", user=self.user_1)
#         self.user_2 = User.objects.create_user(username="authorusername2", email="author@gamil.com", password="authorpassword")
#         self.user_2.save()
#         self.author_id2 = self.authorserializer.create_author("author username2", "author firstname", "author lastname", "author@gamil.com", "authorpassword", user=self.user_2)        
#         self.serializer = FollowerSerializer()
#         self.apiserializer = FollowerAPISerializer()

#     def tearDown(self) -> None:
#         self.user_1.delete()
#         self.user_2.delete()

#     def test_single_follower(self):
        
#         relation_id = self.serializer.create_relations(self.author_id1, self.author_id2)
#         self.serializer.update_follow_status(self.author_id1, self.author_id2, True)
#         follower_data = self.apiserializer.get_single_follower(self.author_id1, self.author_id2)
#         author_id2_data = self.authorapiserializer.get_single_author(self.author_id2)

#         self.assertTrue(author_id2_data["type"] == follower_data["type"])
#         self.assertTrue(author_id2_data["id"] == follower_data["id"])
#         self.assertTrue(author_id2_data["url"] == follower_data["url"])
#         self.assertTrue(author_id2_data["host"] == follower_data["host"])
#         self.assertTrue(author_id2_data["displayName"] == follower_data["displayName"])
#         self.assertTrue(author_id2_data["username"] == follower_data["username"])

#     def test_get_all_followers(self):
#         relation_id = self.serializer.create_relations(self.author_id1, self.author_id2)
#         self.serializer.update_follow_status(self.author_id1, self.author_id2, True)
        
#         followers_data = self.apiserializer.get_all_followers(self.author_id1)
#         author_id2_data = self.authorapiserializer.get_single_author(self.author_id2)

#         self.assertTrue(len(followers_data["items"]) == 1)
#         self.assertTrue(author_id2_data["type"] == followers_data["items"][0]["type"])
#         self.assertTrue(author_id2_data["id"] == followers_data["items"][0]["id"])
#         self.assertTrue(author_id2_data["url"] == followers_data["items"][0]["url"])
#         self.assertTrue(author_id2_data["host"] == followers_data["items"][0]["host"])
#         self.assertTrue(author_id2_data["displayName"] == followers_data["items"][0]["displayName"])
#         self.assertTrue(author_id2_data["username"] == followers_data["items"][0]["username"])

#     def test_without_followers(self):
#         relation_id = self.serializer.create_relations(self.author_id1, self.author_id2)
#         followers_data = self.apiserializer.get_all_followers(self.author_id1)
#         follower_data = self.apiserializer.get_single_follower(self.author_id1, self.author_id2)

#         self.assertTrue(len(followers_data["items"]) == 0)
#         self.assertTrue(follower_data is None)

    # def test_get_single_author(self):
    #     user = User.objects.create_user(username="authorusername", email="author@gamil.com", password="authorpassword")
    #     user.save()

    #     author_id = self.serializer.create_author("authorusername", "author firstname", "author lastname", "author@gmail.com", "authorpassword", user=user)
    #     self.assertTrue(author_id == self.serializer.get_author_id_by_username("authorusername"))

    #     author_obj = self.serializer.get_author_by_id(author_id)

    #     single_author_response = self.apiserializer.get_single_author(author_id)

    #     self.assertTrue(author_obj.id == single_author_response["id"])
    #     self.assertTrue(author_obj.id == author_id)        
    #     self.assertTrue("author" == single_author_response["type"])
    #     self.assertTrue(author_obj.username == single_author_response["username"])
    #     self.assertTrue(author_obj.email == single_author_response["email"])
    #     self.assertTrue(author_obj.name == single_author_response["displayName"])
    #     self.assertTrue(author_obj.host == single_author_response["host"])
    #     user.delete()

    
    # def test_get_all_authors(self):
    #     user1 = User.objects.create_user(username="authorusername1", email="author@gamil.com", password="authorpassword")
    #     user1.save()

    #     author_id1 = self.serializer.create_author("authorusername1", "author firstname", "author lastname", "author@gmail.com", "authorpassword", user=user1)
        
    #     user2 = User.objects.create_user(username="authorusername2", email="author@gamil.com", password="authorpassword")
    #     user2.save()

    #     author_id2 = self.serializer.create_author("authorusername2", "author firstname1", "author lastname1", "author1@gmail.com", "authorpassword1", user=user2)

    #     self.assertTrue(author_id1 == self.serializer.get_author_id_by_username("authorusername1"))
    #     self.assertTrue(author_id2 == self.serializer.get_author_id_by_username("authorusername2"))

    #     first_author_obj = self.serializer.get_author_by_id(author_id1)
    #     second_author_obj = self.serializer.get_author_by_id(author_id2)

    #     all_authors_response = self.apiserializer.get_all_authors()

    #     self.assertTrue("authors" == all_authors_response["type"])
    #     self.assertTrue(2 == len(all_authors_response["items"]))
    #     self.assertTrue(first_author_obj.username == all_authors_response["items"][0]["username"])
    #     self.assertTrue(first_author_obj.id == all_authors_response["items"][0]["id"])
    #     self.assertTrue(first_author_obj.email == all_authors_response["items"][0]["email"])
    #     self.assertTrue(first_author_obj.name == all_authors_response["items"][0]["displayName"])
    #     self.assertTrue(first_author_obj.host == all_authors_response["items"][0]["host"])
    #     self.assertTrue(second_author_obj.username == all_authors_response["items"][1]["username"])
    #     self.assertTrue(second_author_obj.id == all_authors_response["items"][1]["id"])
    #     self.assertTrue(second_author_obj.email == all_authors_response["items"][1]["email"])
    #     self.assertTrue(second_author_obj.name == all_authors_response["items"][1]["displayName"])
    #     self.assertTrue(second_author_obj.host == all_authors_response["items"][1]["host"])

    #     user1.delete()
    #     user2.delete()
