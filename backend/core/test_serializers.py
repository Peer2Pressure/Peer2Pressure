from .models import *
from django.test import TestCase
from .serializers.authorserializer import AuthorSerializer, AllAuthorSerializer
from .serializers.postserializer import PostSerializer
from .serializers.followerserializer import FollowerSerializer, AllFollowerSerializer
from .serializers.commentserializer import CommentSerializer
from .serializers.postlikeserializer import PostLikeSerializer
from django.contrib.auth.models import User, auth
from rest_framework.exceptions import ValidationError

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
    
    def tearDown(self):
        self.author.delete()

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

class AllAuthorSerializerTest(TestCase):
    def setUp(self):
        self.author_data = {
            "name": "Test Author",
            "github": "https://github.com/testauthor",
            "avatar": "https://testauthor.com/avatar.png"
        }
        self.author = Author.objects.create(**self.author_data)

    def test_all_author_serializer(self):
        serializer = AllAuthorSerializer(instance={"items": [self.author]})
        self.assertEqual(serializer.data["items"][0]["displayName"], self.author_data["name"])
        self.assertEqual(serializer.data["items"][0]["github"], self.author_data["github"])

class FollowerSerializerTestCase(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(
        name="John Doe1",
        username="johndoe1",
        email="johndoe1@example.com",
        password="password1",
        github="https://github.com/johndoe1",
        avatar=""
        )

        self.author2 = Author.objects.create(
            name="Jane Doe",
            username="janedoe",
            email="johndoe@example.com",
            password="password",
            github="https://github.com/johndoe",
            avatar=""
        )

        self.follower_data = {
            "from_author": self.author1,
            "to_author": self.author2,
            "approved": True
        }

        self.follower = Follower.objects.create(**self.follower_data)
        print(self.follower)
        print("fromauthor: ", self.follower.from_author)
        print("toauthor: ", self.follower.to_author)

    def tearDown(self):
        self.author1.delete()
        self.author2.delete()
        self.follower.delete()

    def test_get_relation_by_ids(self):
        serializer = FollowerSerializer()
        author1_uuid = self.author1.id.split("/")[-1]
        author2_uuid = self.author2.id.split("/")[-1]
        follower = serializer.get_relation_by_ids(author2_uuid, author1_uuid)
        self.assertEqual(follower, self.follower)

        with self.assertRaises(ValidationError):
            serializer.get_relation_by_ids(self.author1.m_id, self.author1.m_id)
    
    def test_follower_exists(self):
        serializer = FollowerSerializer()
        author1_uuid = self.author1.id.split("/")[-1]
        author2_uuid = self.author2.id.split("/")[-1]
        self.assertTrue(serializer.follower_exists(author2_uuid, author1_uuid))
        self.assertFalse(serializer.follower_exists(author1_uuid, author2_uuid))

    def test_update(self):
        serializer = FollowerSerializer()
        data = {'approved': True}
        instance = serializer.update(self.follower, data)
        self.assertEqual(instance.approved, True)

class PostSerializerTestCase(TestCase):
    def setUp(self):
        self.author_data = {
                "type": "author",
                "id": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff",
                "url": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff",
                "host": "https://p2psd.herokuapp.com",
                "displayName": "Vivian",
                "github": "",
                "profileImage": ""
            }
        
        validated_author = AuthorSerializer(data=self.author_data)
        validated_author.is_valid(raise_exception=True)
        self.author = validated_author.save()

        self.post_data = {
            "type": "post",
            "title": "Another test",
            "id": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff/posts/52cfadc1-548f-45f2-8fa4-286272f568cd",
            "source": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff/posts/52cfadc1-548f-45f2-8fa4-286272f568cd",
            "origin": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff/posts/52cfadc1-548f-45f2-8fa4-286272f568cd",
            "description": "",
            "contentType": "text/plain",
            "content": "more tests",
            "author": {
                "type": "author",
                "id": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff",
                "url": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff",
                "host": "https://p2psd.herokuapp.com",
                "displayName": "Vivian",
                "github": "",
                "profileImage": ""
            },
            "comments": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff/posts/52cfadc1-548f-45f2-8fa4-286272f568cd/comments",
            "published": "2023-04-03T05:28:56.129880Z",
            "visibility": "PUBLIC",
        }

    def tearDown(self):
        Post.objects.filter(id=self.post_data["id"]).delete()


    def test_post_serializer(self):
        serializer = PostSerializer(data=self.post_data)
        self.assertTrue(serializer.is_valid())

    def test_post_serializer_invalid(self):
        invalid_post_data = {
            "type": "post",
            "title": "Another test",
            "id": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff/posts/52cfadc1-548f-45f2-8fa4-286272f568cd",
            "source": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff/posts/52cfadc1-548f-45f2-8fa4-286272f568cd",
            "origin": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff/posts/52cfadc1-548f-45f2-8fa4-286272f568cd",
            "description": "",
            "contentType": "text/plain",
            "content": "more tests",
            "author": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff",
            "comments": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff/posts/52cfadc1-548f-45f2-8fa4-286272f568cd/comments",
            "published": "2023-04-03T05:28:56.129880Z",
            "visibility": "PUBLIC",
        }
        serializer = PostSerializer(data=invalid_post_data)
        self.assertFalse(serializer.is_valid())

    def test_post_exists(self):
        serializer = PostSerializer()
        post_uuid = self.post_data["id"].split("/")[-1]
        self.assertFalse(serializer.post_exists(post_id = post_uuid, author_id = self.author_data["id"].split("/")[-1]))

    def test_update_post(self):
        serializer = PostSerializer()
        post_uuid = self.post_data["id"].split("/")[-1]
        self.assertFalse(serializer.update_post(post_id = post_uuid, author_id = self.author_data["id"].split("/")[-1], defaults = self.post_data))

    def test_delete_post(self):
        serializer = PostSerializer()
        post_uuid = self.post_data["id"].split("/")[-1]
        self.assertFalse(serializer.delete_post(post_id = post_uuid, author_id = self.author_data["id"].split("/")[-1]))

    # def test_create(self):
    #     validated_data = PostSerializer(data=self.post_data)
    #     serializer = PostSerializer()
    #     author_serializer = AuthorSerializer()
    #     author = author_serializer.get_author_by_id(author_id = self.author_data["id"].split("/")[-1])
    #     self.assertTrue(validated_data.is_valid())

    #     validated_data["author"] = author
    #     validated_data.save()
        
        # self.assertEqual(validated_data.title, self.post_data['title'])

# class AllFollowerSerializerTestCase(TestCase):
#     def setUp(self) -> None:
#         self.author1 = Author.objects.create(
#             name="John Doe1",
#             username="johndoe1",
#             email="johndoe1@example.com",
#             password="password1",
#             github="https://github.com/johndoe1",
#             avatar=""
#         )

#         self.author2 = Author.objects.create(
#             name="Jane Doe",
#             username="janedoe",
#             email="johndoe@example.com",
#             password="password",
#             github="https://github.com/johndoe",
#             avatar=""
#         )

#         self.follower_data = {
#             "from_author": self.author1,
#             "to_author": self.author2,
#             "approved": True
#         }
 
#         self.follower = Follower.objects.create(**self.follower_data)


    # def test_to_representation(self):
    #     # serializer = AllFollowerSerializer(instance=[self.author1, self.author2])
    #     serializer = AllFollowerSerializer(instance=self.follower)
    #     data = serializer.to_representation(serializer.instance)
    #     print("result of follower: ", data)



'''
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