from .models import *
from django.test import TestCase
from .serializers import *

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
        # print(author_id)

class PostSerializerTest(TestCase):
    def setUp(self) -> None:
        self.authorserializer = AuthorSerializer()
        self.author_id = self.authorserializer.create_author("author username", "author firstname", "author lastname", "author@gamil.com", "authorpassword")        
        self.serializer = PostSerializer()

    def test_post_create(self):
        post_id = self.serializer.create_post(self.author_id, False, caption="POST Caption")
        created_post = Post.objects.get(id=post_id)
        self.assertTrue(created_post.caption == "POST Caption")
        self.assertTrue(not created_post.is_private)

class RelationsSerializerTest(TestCase):
    def setUp(self) -> None:
        self.authorserializer = AuthorSerializer()
        self.author_id1 = self.authorserializer.create_author("author username1", "author firstname", "author lastname", "author@gamil.com", "authorpassword")        
        self.author_id2 = self.authorserializer.create_author("author username2", "author firstname", "author lastname", "author@gamil.com", "authorpassword")        
        self.serializer = RelationsSerializer()

    def test_relation_create (self):
        relation_id = self.serializer.create_relations(self.author_id1, self.author_id2)
        created_relation = Relations.objects.get(id=relation_id)
        self.assertTrue(relation_id == created_relation.id)
