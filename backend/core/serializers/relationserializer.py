# Local libraries
from .. models import *

# Third-party libraries
from rest_framework import serializers
from varname import nameof        

from django.db.models import Q

class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = "__all__"

    def create_relations(self, author_id, foreign_author_id):

        try:
            from_author_obj = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            raise ValueError("From Author does not exist")
        
        try:
            to_author_obj = Author.objects.get(pk=foreign_author_id)
        except Author.DoesNotExist:
            raise ValueError("To Author does not exist")
        
        defaults = {
            nameof(Relation.from_author): from_author_obj,
            nameof(Relation.to_author): to_author_obj
        }

        relation_obj= Relation.objects.create(**defaults)

        return relation_obj
    
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
    
    def get_followers(self, author_id):
        to_relations = Relation.objects.filter(to_author_id=author_id, to_author_request=True)
        from_relations = Relation.objects.filter(from_author_id=author_id, from_author_request=True)

        followers = []

        for follower in to_relations:
            followers.append(follower.from_author)

        for follower in from_relations:
            follower.append(follower.to_author)

        return followers