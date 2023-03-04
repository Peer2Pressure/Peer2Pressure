from rest_framework import serializers
from . models import *
from varname import nameof
from .serializers.authorserializer import AuthorSerializer
from .serializers.relationserializer import RelationSerializer
from .serializers.postserializer import PostSerializer


author_serializer = AuthorSerializer()
relation_serializer = RelationSerializer()
post_serializer = PostSerializer()

class AuthorAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def get_author_data(self, author):
        author_data = {
            "type": "author",
            "id": author.id,
            "url": author.url,
            "host": author.host,
            "displayName": f"{author.first_name} {author.last_name}",
            "username": author.username,
            "email": author.email,
            "profileImage": f"{author.host}{author.avatar.url}",
            }
        return author_data
    
    def get_single_author(self, author_id):
        author_data = {}
        try:
            author = author_serializer.get_author_by_id(author_id)
            author_data = self.get_author_data(author)
        except ValueError:
            return None
        return author_data
    
    def get_all_authors(self):

        authors = Author.objects.all()
        
        result_dict = {}
        result_dict["type"] = "authors"

        authors_list = []

        for author in authors:
            curr_author_data = self.get_author_data(author)
            authors_list.append(curr_author_data)

        result_dict["items"] = authors_list

        return result_dict

    def create_or_update_author(self, author_id, request_data):
        author = None
        updatable_fields = ["first_name", "last_name", "username", "email", "avatar"]
        try:
            author = author_serializer.get_author_by_id(author_id=author_id)
        except ValueError:
            # TODO : If author does not exist create new author. Will need to create new User object too !!!
            # author = author_serializer.create_author()
            return None

        defaults = {}
        for key in request_data:
            if key in updatable_fields:
                defaults[key] = request_data[key]

        Author.objects.filter(pk=author_id).update(**defaults)

        return self.get_single_author(author_id)


author_api_serializer = AuthorAPISerializer()

class RelationAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = "__all__"

    
    def get_all_followers(self, author_id):
        follower_relations = None
        try:
            follower_relations = author_serializer.get_author_by_id(author_id).follower.all()
        except ValueError:
            return None
        
        followers = [follower.from_author for follower in follower_relations]

        result_dict = {}
        result_dict["type"] = "followers"

        followers_list = []

        for follower in followers:
            follower_serialized = author_api_serializer.get_author_data(follower)
            followers_list.append(follower_serialized)

        result_dict["items"] = followers_list

        return result_dict

    def get_single_follower(self, author_id, foreign_author_id):
        relation = None
        try:
            relation = relation_serializer.get_relation_by_ids(author_id, foreign_author_id)
        except ValueError:
            return None
        
        follower = relation.from_author
        follower_serialized = author_api_serializer.get_author_data(follower)

        return follower_serialized

    def remove_follower(self, author_id, foreign_author_id):
        relation = None
        try:
            relation = relation_serializer.get_relation_by_ids(author_id, foreign_author_id)
        except ValueError:
            return None
        
        relation.delete()

        return relation


class PostAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def get_post_data(self, post):
        author_data = author_api_serializer.get_author_data(post.author)

        post_data = {
            "type": "post",
            "id": post.id,
            "url": post.url,
            "title": post.title,
            "content": post.content,
            "visibility": "private"if post.is_private else "public", 
            "image": f"{author_data['host']}{post.image.url}" if post.image else None,
            "author": author_data,
            }
        
        return post_data
    
    # def create_post(self, author_id)


    def get_all_author_posts(self, author_id):
        author = None
        try:
            author = author_serializer.get_author_by_id(author_id)
        except ValueError:
            return None
        
        posts = Post.objects.filter(author=author)

        result_dict = {}
        result_dict["type"] = "posts"

        posts_list = []

        for post in posts:
            curr_post_data = self.get_post_data(post)
            posts_list.append(curr_post_data)

        result_dict["items"] = posts_list

        return result_dict
    
    def get_a_post(self, authorid, postid):
        result_dict = {}

        result_dict["type"] = "post"
        # TODO: Need to add title to POST Model
        result_dict["title"] = ""

        # TODO: Need to handle the case if post or author doesn't exist
        post_obj = post_serializer.get_post(authorid, postid)
        author = author_serializer.get_author_by_id(authorid)

        result_dict["id"] = str(author.host) + "/authors/" + str(authorid) + "/posts/" + str(postid)

        # TODO: Need to find source and origin
        result_dict["origin"] = ""
        result_dict["source"] = ""

        # TODO: Need to add Description for POST Model
        result_dict["description"] = ""

        # TODO: Need to support multiple formats
        result_dict["contentType"] = "text/plain"

        result_dict["content"] = post_obj.caption

        result_dict["author"] = author_api_serializer.get_single_author(authorid)

        # TODO: Need to add way to organize the post to categories
        result_dict["categories"] = []

        # TODO: Need to get the serailzier with get_count for number of comments for post
        result_dict["count"] = 0

        # TODO: Need to get the first page of comments
        result_dict["comments"] = ""

        # TODO: Need to convert the created_at to ISO 8601 TIMESTAMP
        result_dict["published"] = post_obj.created_at

        # TODO: Need to set the visibility to actual visibility
        result_dict["visibility"] = "PUBLIC"

        # TODO: Need to find what unlisted mean
        result_dict["unlisted"] = False

        return result_dict
