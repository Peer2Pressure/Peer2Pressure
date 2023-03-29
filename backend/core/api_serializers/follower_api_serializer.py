import json
import pprint
import uuid
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

        serializer = FollowerSerializer(follow)
        
        return serializer.data, 200

    def create_follow_request(self, author_id, foreign_author_id, request_data):
        # if not author_serializer.author_exists(author_id):
        #     return {"msg": "Author does not exist"}, 404
        follow_serializer= FollowerSerializer(data=request_data)
        if follow_serializer.is_valid():
            validated_follower_data = follow_serializer.validated_data
            follow = None
            if follower_serializer.follower_exists(author_id, foreign_author_id):
                if not validated_follower_data["approved"]:
                    return {"msg": f"Friend request already send. Cannot send again."}, 400

                follow = follower_serializer.get_relation_by_ids(author_id, foreign_author_id)
                if follow.approved:
                    return {"msg": f"{foreign_author_id} already follows {author_id}"}, 400
                validated_follower_data["m_id"] = follow.m_id
            else:
                # Make sure other authors cannot override local author approval
                validated_follower_data["approved"] = False

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
            validated_follower_data["from_author"] = foreign_author
            validated_follower_data["to_author"] = author

            if not follow_serializer.follower_exists(author_id, foreign_author_id):
                validated_follower_data["m_id"] = uuid.uuid4()
                follow_serializer.save()
            else:
                follow = follow_serializer.get_relation_by_ids(author_id, foreign_author_id)
                follow = follow_serializer.update(follow, validated_follower_data)
                if validated_follower_data["approved"]:
                    return {"msg": f"Follow request from {foreign_author_id} has been approved."}, 200
        else:
            return serializer.errors, 400
                
        return {"msg": f"Follow request has been send to {author_id}"}, 200


    def remove_follower(self, author_id, foreign_author_id):
        if not follower_serializer.follower_exists(author_id, foreign_author_id):
            return {"msg": "Follow relation does not exist"}, 404
        
        follow = follower_serializer.get_relation_by_ids(author_id, foreign_author_id)

        follow.delete()

        return {"msg": f"{foreign_author_id} has unfollwed {author_id}"}, 200