from .models import *
from django.test import TestCase
from .serializers.authorserializer import AuthorSerializer
from .serializers.postserializer import PostSerializer
from .serializers.relationserializer import RelationSerializer
from .serializers.commentserializer import CommentSerializer
from .serializers.likeserializer import LikeSerializer

class AuthorSerializerTest(TestCase):
    def setUp(self) -> None:
        self.serializer = AuthorSerializer()

    def test_author_create(self):
        author_id = self.serializer.create_author("author username", "author firstname", "author lastname", "author@gamil.com", "authorpassword")
        created_author = Author.objects.get(id=author_id)
        self.assertTrue(created_author.username == "author username")
        self.assertTrue(created_author.first_name == "author firstname")
        self.assertTrue(created_author.last_name == "author lastname")
        self.assertTrue(created_author.email == "author@gamil.com")
        self.assertTrue(created_author.password == "authorpassword")
        
        self.assertTrue(self.serializer.get_author_id_by_username(created_author.username) == author_id)

    def test_get_author(self):
        author_id = self.serializer.create_author("author username", "author firstname", "author lastname", "author@gamil.com", "authorpassword")

        self.assertTrue(author_id == self.serializer.get_author_id_by_username("author username"))

        author_obj = self.serializer.get_author_by_id(author_id)

        self.assertTrue(author_id == author_obj.id)

        self.assertTrue(author_obj.username == "author username")

class RelationSerializerTest(TestCase):
    def setUp(self) -> None:
        self.authorserializer = AuthorSerializer()
        self.author_id1 = self.authorserializer.create_author("author username1", "author firstname", "author lastname", "author@gamil.com", "authorpassword")        
        self.author_id2 = self.authorserializer.create_author("author username2", "author firstname", "author lastname", "author@gamil.com", "authorpassword")        
        self.serializer = RelationSerializer()

    def test_relation_create(self):
        relation_id = self.serializer.create_relations(self.author_id1, self.author_id2)
        # relation_obj = Relation.objects.get(id = relation_id)
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
