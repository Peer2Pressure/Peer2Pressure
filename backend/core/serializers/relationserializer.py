# Third-party libraries
from rest_framework import serializers
from varname import nameof

# Local libraries
from .. models import *
from ..serializers.authorserializer import AuthorSerializer
from ..api_serializers import *

author_serializer = AuthorSerializer()

class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = "__all__"

    def create_relations(self, author_id, foreign_author_id):
    
        try:
            from_author_obj = author_serializer.get_author_by_id(foreign_author_id)
        except ValueError:
            return None

        try:
            to_author_obj = author_serializer.get_author_by_id(author_id)
        except ValueError:
            return None
        
        try:
            relation = self.get_relation_by_ids(author_id, foreign_author_id)
        except ValueError:
            defaults = {
                nameof(Relation.from_author): from_author_obj,
                nameof(Relation.to_author): to_author_obj
            }
            relation_obj = Relation.objects.create(**defaults)

            return relation_obj.id

        return None

    def update_follow_status(self, from_authorid, to_authorid, status):

        relation = Relation.objects.filter(to_author_id = to_authorid, from_author_id = from_authorid, to_author_request = not status)

        if len(relation) > 0:
            relation.update(to_author_request = status)
            return True
        
        relation = Relation.objects.filter(from_author_id = to_authorid, to_author_id = from_authorid, from_author_request = not status)

        if len(relation) > 0:
            relation.update(from_author_request = status)
            return True
        
        raise ValueError("Relation doesn't exist")
    
    def check_follow_status(self, from_authorid, to_authorid):

        relation = Relation.objects.filter(to_author_id = to_authorid, from_author_id = from_authorid, to_author_request = True)

        if len(relation) > 0:
            return True
        
        relation = Relation.objects.filter(from_author_id = to_authorid, to_author_id = from_authorid, from_author_request = True)

        if len(relation) > 0:
            return True
        
        return False        
    
    def get_relation_by_ids(self, author_id, foreign_author_id):
        relation = None
        try:
            relation = Relation.objects.get(from_author=foreign_author_id, to_author=author_id)
        except Relation.DoesNotExist:
            raise ValueError("Relation does not exist")

        return relation
    
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
            follower_serialized = author_serializer.get_author_data(follower)
            followers_list.append(follower_serialized)

        result_dict["items"] = followers_list

        return result_dict

    def get_single_follower(self, author_id, foreign_author_id):
        relation = None
        try:
            relation = self.get_relation_by_ids(author_id, foreign_author_id)
        except ValueError:
            return None
        
        follower = relation.from_author
        follower_serialized = author_serializer.get_author_data(follower)

        return follower_serialized

    def remove_follower(self, author_id, foreign_author_id):
        relation = None
        try:
            relation = self.get_relation_by_ids(author_id, foreign_author_id)
        except ValueError:
            return None
        
        relation.delete()

        return relation
