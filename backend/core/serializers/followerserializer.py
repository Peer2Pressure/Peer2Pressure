# Third-party libraries
from rest_framework import serializers
from varname import nameof

# Local libraries
from ..models import *
from .authorserializer import AuthorSerializer

author_serializer = AuthorSerializer()

class FollowerSerializer(serializers.ModelSerializer):
    type = serializers.CharField(required=False, max_length=10, default="follow", read_only=True)
    summary = serializers.CharField(required=False, read_only=True)
    actor = AuthorSerializer()
    object = AuthorSerializer()

    class Meta:
        model = Follower
        fields = ["type", "summary", "actor", "object"]

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
                nameof(Follower.from_author): from_author_obj,
                nameof(Follower.to_author): to_author_obj
            }
            relation_obj = Follower.objects.create(**defaults)

            return relation_obj.id

        return None

    def update_follow_status(self, from_authorid, to_authorid, status):

        relation = Follower.objects.filter(to_author_id = to_authorid, from_author_id = from_authorid, to_author_request = not status)

        if len(relation) > 0:
            relation.update(to_author_request = status)
            return True
        
        relation = Follower.objects.filter(from_author_id = to_authorid, to_author_id = from_authorid, from_author_request = not status)

        if len(relation) > 0:
            relation.update(from_author_request = status)
            return True
        
        raise ValueError("Follower doesn't exist")
    
    def check_follow_status(self, from_authorid, to_authorid):

        relation = Follower.objects.filter(to_author_id = to_authorid, from_author_id = from_authorid, to_author_request = True)

        if len(relation) > 0:
            return True
        
        relation = Follower.objects.filter(from_author_id = to_authorid, to_author_id = from_authorid, from_author_request = True)

        if len(relation) > 0:
            return True
        
        return False        
    
    def get_relation_by_ids(self, author_id, foreign_author_id):
        relation = None
        try:
            relation = Follower.objects.get(from_author=foreign_author_id, to_author=author_id)
        except Follower.DoesNotExist:
            raise ValueError("Follower does not exist")

        return relation