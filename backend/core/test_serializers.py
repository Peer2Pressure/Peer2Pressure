from .models import *
from django.test import TestCase
from .serializers.authorserializer import AuthorSerializer, AllAuthorSerializer
from .serializers.postserializer import PostSerializer
from .serializers.followerserializer import FollowerSerializer
from .serializers.commentserializer import CommentSerializer
from .serializers.postlikeserializer import PostLikeSerializer
from django.contrib.auth.models import User, auth

class AuthorSerializerTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe",
            username="johndoe",
            email="johndoe@example.com",
            password="password",
            github="https://github.com/johndoe",
            avatar=""
        )

    def test_author_serializer(self):
        serializer = AuthorSerializer(instance=self.author)
        expected_data = {
            "type": "author",
            "id": str(self.author.id),
            "url": str(self.author.url),
            "host": str(self.author.host),
            "displayName": "John Doe",
            "github": "https://github.com/johndoe",
            "profileImage": "",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_author_serializer_update(self):
        data = {
            "github": "https://github.com/janedoe",
            "avatar": ""
        }
        serializer = AuthorSerializer(instance=self.author, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.author.refresh_from_db()
        self.assertEqual(self.author.github, "https://github.com/janedoe")
        self.assertEqual(self.author.avatar, "")

    def test_author_serializer_get_author_by_id(self):
        serializer = AuthorSerializer()
        author_uuid = self.author.id.split("/")[-1]
        author_obj = serializer.get_author_by_id(author_uuid)
        self.assertEqual(author_obj, self.author)

    def test_author_serializer_get_author_id_by_username(self):
        serializer = AuthorSerializer()
        author_id = serializer.get_author_id_by_username(self.author.username)
        self.assertEqual(author_id, self.author.id)

    def test_author_serializer_author_exists(self):
        serializer = AuthorSerializer()
        author_uuid = self.author.id.split("/")[-1]
        self.assertTrue(serializer.author_exists(author_uuid))
        self.assertFalse(serializer.author_exists(999))

# class AllAuthorSerializerTest(TestCase):
#     def setUp(self):
#         self.author_data = {
#             "name": "Test Author",
#             "github": "https://github.com/testauthor",
#             "avatar": "https://testauthor.com/avatar.png"
#         }
#         self.author = Author.objects.create(**self.author_data)

#     def test_all_author_serializer(self):
#         serializer = AllAuthorSerializer(instance={"items": [self.author]})
#         self.assertEqual(serializer.data["items"][0]["name"], self.author_data["name"])
#         self.assertEqual(serializer.data["items"][0]["github"], self.author_data["github"])
#         self.assertEqual(serializer.data["items"][0]["avatar"], self.author_data["avatar"])

'''
# class AuthorSerializerTest(TestCase):
#     def setUp(self):
#         self.author_data = {
#             "username": "authorusername",
#             "name": "author name",
#             "email": "author@gmail.com",
#             "password": "authorpassword",
#         }
#         self.author = Author.objects.create(**self.author_data)

#         self.serializer = AuthorSerializer(instance=self.author)

#     def test_author_serialization(self):
#         expected_data = {
#             "type": "author",
#             "id": str(self.author.id),
#             "url": f"http://testserver/api/v1/authors/{self.author.id}",
#             "host": None,
#             "displayName": "author name",
#             "github": None,
#             "profileImage": None,
#         }
#         self.assertEqual(self.serializer.data, expected_data)

#     def test_author_deserialization(self):
#         author_data = {
#             "username": "newusername",
#             "name": "new name",
#             "email": "newemail@gmail.com",
#             "password": "newpassword",
#         }
#         serializer = AuthorSerializer(data=author_data)
#         self.assertTrue(serializer.is_valid())

#         author = serializer.save()
#         self.assertTrue(Author.objects.filter(id=author.id).exists())
#         self.assertEqual(author.username, author_data["username"])
#         self.assertEqual(author.name, author_data["name"])
#         self.assertEqual(author.email, author_data["email"])
#         self.assertEqual(author.password, author_data["password"])

#     def tearDown(self):
#         self.author.delete()

class FollowerSerializerTest(TestCase):
    def setUp(self) -> None:
        self.authorserializer = AuthorSerializer()
        user1 = User.objects.create_user(username="authorusername1", email="author@gamil.com", password="authorpassword")
        user1.save()
        self.author_id1 = self.authorserializer.create_author("authorusername1", "author firstname", "author lastname", "author@gamil.com", "authorpassword", user=user1)
        user2 = User.objects.create_user(username="authorusername2", email="author@gamil.com", password="authorpassword")
        user2.save()
        self.author_id2 = self.authorserializer.create_author("author username2", "author firstname", "author lastname", "author@gamil.com", "authorpassword", user=user2)        
        self.serializer = FollowerSerializer()

    def tearDown(self) -> None:
        self.user_1.delete()
        self.user_2.delete()

    def test_relation_create(self):
        relation_id = self.serializer.create_relations(self.author_id1, self.author_id2)
        # relation_obj = Follower.objects.get(id = relation_id)
        created_relation = self.serializer.get_relation_by_ids(self.author_id1, self.author_id2)
        self.assertTrue(relation_id == created_relation.id)
        self.assertTrue(not created_relation.from_author_request)
        self.assertTrue(not created_relation.to_author_request)

    def test_check_follow_status(self):
        relation_id = self.serializer.create_relations(self.author_id1, self.author_id2)
        created_relation = self.serializer.get_relation_by_ids(self.author_id1, self.author_id2)
        self.assertTrue(relation_id == created_relation.id)
        self.assertTrue(not created_relation.from_author_request)
        self.assertTrue(not created_relation.to_author_request)
        self.assertTrue(not self.serializer.check_follow_status(self.author_id1, self.author_id2))

    def test_update_follow_status(self):
        relation_id = self.serializer.create_relations(self.author_id1, self.author_id2)
        created_relation = self.serializer.get_relation_by_ids(self.author_id1, self.author_id2)
        self.assertTrue(relation_id == created_relation.id)
        self.assertTrue(not created_relation.from_author_request)
        self.assertTrue(not created_relation.to_author_request)
        self.assertTrue(not self.serializer.check_follow_status(self.author_id1, self.author_id2))
        self.assertTrue(self.serializer.update_follow_status(self.author_id1, self.author_id2, True))
        self.assertTrue(self.serializer.check_follow_status(self.author_id1, self.author_id2))

    # def test_get_all_followers(self):
    #     relation_id = self.serializer.create_relations(self.author_id1, self.author_id2)
    #     created_relation = self.serializer.get_relation_by_ids(self.author_id1, self.author_id2)
    #     self.assertTrue(relation_id == created_relation.id)
    #     self.assertTrue(not created_relation.from_author_request)
    #     self.assertTrue(not created_relation.to_author_request)
    #     self.assertTrue(not self.serializer.check_follow_status(self.author_id1, self.author_id2))
    #     self.assertTrue(self.serializer.update_follow_status(self.author_id1, self.author_id2, True))
    #     self.assertTrue(self.serializer.check_follow_status(self.author_id1, self.author_id2))

    #     all_follower_response = self.serializer.get_all_followers(self.author_id1)

    #     self.assertTrue(len(all_follower_response["items"]) == 1)

# class PostSerializerTest(TestCase):
#     def setUp(self) -> None:
#         self.authorserializer = AuthorSerializer()
#         self.author_id = self.authorserializer.create_author("author username", "author firstname", "author lastname", "author@gamil.com", "authorpassword")        
#         self.serializer = PostSerializer()

    # def test_post_create(self):
    #     # post_id = self.serializer.create_post(self.author_id, {})
    #     # post_id = self.serializer.create_post(self.author_id, False, caption="POST Caption")
    #     created_post = Post.objects.get(id=post_id)
    #     self.assertTrue(created_post.caption == "POST Caption")
    #     self.assertTrue(not created_post.is_private)
'''