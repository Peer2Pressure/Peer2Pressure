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
        self.author_serializer = AuthorSerializer()
        self.author_saved_data = self.author_serializer.get_author_by_id(self.author.m_id)
        # self.author_saved_data = self.author_serializer.get_author_by_id(self.author.id.split("/")[-1])

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
        self.author.delete()


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
        
    def test_post_create(self):
        serializer = PostSerializer(data=self.post_data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        validated_data["author"] = self.author_saved_data
        validated_data["m_id"] = self.post_data["id"].split("/")[-1]
        post = serializer.create(validated_data)
        self.assertEqual(post.title, self.post_data['title'])
        self.assertEqual(post.content, self.post_data['content'])
        self.assertEqual(post.description, self.post_data['description'])
        self.assertEqual(post.visibility, self.post_data['visibility'])
        self.assertEqual(post.author, self.author_saved_data)

class PostLikeSerializerTest(TestCase):

    def test_post_like_serializer(self):
        post_like_data = {
            "type": "like",
            "summary": "Vivian liked your post",
            "author": {
                "type": "author",
                "id": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff",
                "url": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff",
                "host": "https://p2psd.herokuapp.com",
                "displayName": "Vivian",
                "github": "",
                "profileImage": ""
            },
            "object": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff/posts/52cfadc1-548f-45f2-8fa4-286272f568cd",
        }
        serializer = PostLikeSerializer(data=post_like_data)
        self.assertTrue(serializer.is_valid())


class PostCommentSerializerTest(TestCase):

    def test_post_coment_serializer(self):
        post_comment_data = {
            "type": "comment",
            "author": {
                "type": "author",
                "id": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff",
                "url": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff",
                "host": "https://p2psd.herokuapp.com",
                "displayName": "Vivian",
                "github": "",
                "profileImage": ""
            },
            "comment": "This is a comment",
            "contentType": "text/plain",
            "object": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff/posts/52cfadc1-548f-45f2-8fa4-286272f568cd",
        }

        serializer = CommentSerializer(data=post_comment_data)
        self.assertTrue(serializer.is_valid())

    def test_get_comment_post(self):
        post_comment_data = {
            "type": "comment",
            "author": {
                "type": "author",
                "id": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff",
                "url": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff",
                "host": "https://p2psd.herokuapp.com",
                "displayName": "Vivian",
                "github": "",
                "profileImage": ""
            },
            "comment": "This is a comment",
            "contentType": "text/plain",
            "object": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff/posts/52cfadc1-548f-45f2-8fa4-286272f568cd",
        }

        serializer = CommentSerializer(data=post_comment_data)
        self.assertTrue(serializer.is_valid())
        try:
            post = serializer.get_comment_post(comment_id = post_comment_data["object"].split("/")[-1])
        except ValueError as e:
            self.assertTrue(str(e) == "Comment does not exist.")

    def test_get_comment_by_id(self):
        post_comment_data = {
            "type": "comment",
            "author": {
                "type": "author",
                "id": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff",
                "url": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff",
                "host": "https://p2psd.herokuapp.com",
                "displayName": "Vivian",
                "github": "",
                "profileImage": ""
            },
            "comment": "This is a comment",
            "contentType": "text/plain",
            "object": "https://p2psd.herokuapp.com/authors/758be09e-e78d-411c-87cd-a5d9c9d816ff/posts/52cfadc1-548f-45f2-8fa4-286272f568cd",
        }
        serializer = CommentSerializer(data=post_comment_data)
        self.assertTrue(serializer.is_valid())
        try:
            comment = serializer.get_comment_by_id(comment_id = post_comment_data["object"].split("/")[-1])
        except ValueError as e:
            self.assertTrue(str(e) == "Comment does not exist")



    # def test_get_author_post(self):
    #     serializer = PostSerializer(data=self.post_data)
    #     self.assertTrue(serializer.is_valid())
    #     validated_data = serializer.validated_data
    #     validated_data["author"] = self.author_saved_data
    #     validated_data["m_id"] = self.post_data["id"].split("/")[-1]
    #     post = serializer.create(validated_data)
    #     post_uuid = post.id.split("/")[-1]
    #     print("Post authro", post.author)
    #     print(post.author.id.split("/")[-1])
    #     author_serializer = AuthorSerializer()
    #     print("Author saved data", self.author_saved_data)
    #     print("Author saved data id", self.author_saved_data.id)
    #     # print("Author saved data", author_serializer.get_author_by_id(author_id = post.author.id.split("/")[-1]))
    #     # post = serializer.get_author_post(post_id = post_uuid, author_id = post.author.id.split("/")[-1])
    #     # post = serializer.get_author_post(post_id = post_uuid, author_id = self.author_saved_data.id.split("/")[-1])
    #     print("POST: ", post)
    #     # self.assertFalse(serializer.get_author_post(post_id = post_uuid, author_id = post.author.id.split("/")[-1]))


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
