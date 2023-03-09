# Third-party libraries
from rest_framework import serializers

# Local libraries
from ..models import *
from .author_api_serializer import AuthorAPISerializer
from ..serializers.authorserializer import AuthorSerializer
from ..serializers.relationserializer import RelationSerializer

# Model Serializers 
author_serializer = AuthorSerializer()
relation_serializer = RelationSerializer()

# API serializers
author_api_serializer = AuthorAPISerializer()


class RelationAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = "__all__"
    
    def get_all_followers(self, author_id):
        """
        Returns a dictionary containing all the follower of author with author_id
        
        Params:
            author_id (str): uuid of the the author 
        """
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