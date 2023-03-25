import json
import pprint
# Third-party libraries
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Local libraries
from ..models import *
from .author_api_serializer import AuthorAPISerializer
from ..serializers.authorserializer import AuthorSerializer
from ..serializers.followerserializer import FollowerSerializer, AllFollowerSerializer

# Model Serializers 
author_serializer = AuthorSerializer()
follower_serializer = FollowerSerializer()

# API serializers
author_api_serializer = AuthorAPISerializer()


pp = pprint.PrettyPrinter()

class FollowerAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"
    
    def get_all_followers(self, author_id):
        """
        Returns a dictionary containing all the follower of author with author_id
        
        Params:
            author_id (str): uuid of the the author 
        """
        followers = None
        try:
            followers = author_serializer.get_author_by_id(author_id).follower.filter(approved=True)
        except ValidationError as e:
            return {"msg": str(e)}, 404
        
        followers = [follower.from_author for follower in followers]

        post_serializer = AuthorSerializer(followers, many=True)

        serializer = AllFollowerSerializer(data={
                        'items': post_serializer.data
                    })

        if serializer.is_valid():
            return serializer.data, 200
        else:
            return serializer.errors, 400

    def get_single_follower(self, author_id, foreign_author_id):
        if not follower_serializer.follower_exists(author_id, foreign_author_id):
            return {"msg": "Follow relation does not exist"}, 404
        
        follow = follower_serializer.get_relation_by_ids(author_id, foreign_author_id)
        
        follower = follow.from_author
        serializer = AuthorSerializer(follower)
        
        return serializer.data, 200

    def create_follow_request(self, author_id, foreign_author_id, request_data):
        # if not author_serializer.author_exists(author_id):
        #     return {"msg": "Author does not exist"}, 404
        serializer = FollowerSerializer(data=request_data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            if follower_serializer.follower_exists(author_id, foreign_author_id):
                if not validated_data["approved"]:
                    return {"msg": f"Friend request already send. Cannot send again."}, 400

                follow = follower_serializer.get_relation_by_ids(author_id, foreign_author_id)
                if follow.approved:
                    return {"msg": f"{foreign_author_id} already follows {author_id}"}, 400
                
            # If follow request is from a different server, validate and create
            # an author profile for foreign author.
            if not author_serializer.author_exists(foreign_author_id):
                serializer = AuthorSerializer(data=request_data["actor"])            
                if serializer.is_valid():
                    validated_data = serializer.validated_data
                    validated_data["m_id"] = foreign_author_id
                    serializer.save()
                else:
                    return serializer.errors, 400
            
            # If request is from current server to a different server, validate and 
            # create an author profile if it doesn't exist. 
            if not author_serializer.author_exists(author_id):
                serializer = AuthorSerializer(data=request_data["object"])            
                if serializer.is_valid():
                    validated_data = serializer.validated_data
                    validated_data["m_id"] = author_id
                    serializer.save()
                else:
                    return serializer.errors, 400

            author = author_serializer.get_author_by_id(author_id)
            foreign_author = author_serializer.get_author_by_id(foreign_author_id)

            # Update data
            validated_data["from_author"] = foreign_author
            validated_data["to_author"] = author
            serializer.save()
        else:
            return serializer.errors, 400
                
        return {"msg": f"Follow request has been send to {author_id}"}, 200


    def remove_follower(self, author_id, foreign_author_id):
        if not follower_serializer.follower_exists(author_id, foreign_author_id):
            return {"msg": "Follow relation does not exist"}, 404
        
        follow = follower_serializer.get_relation_by_ids(author_id, foreign_author_id)
        
        
        follow.delete()

        return follow, 200