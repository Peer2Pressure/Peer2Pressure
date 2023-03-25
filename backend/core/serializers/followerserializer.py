# Third-party libraries
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from varname import nameof

# Local libraries
from ..models import *
from .authorserializer import AuthorSerializer

author_serializer = AuthorSerializer()

class FollowerSerializer(serializers.ModelSerializer):
    type = serializers.CharField(required=False, max_length=10, default="follow", read_only=True)
    summary = serializers.CharField(required=False)
    actor = AuthorSerializer(source="from_author", required=True)
    object = AuthorSerializer(source="to_author", required=True)
    approved = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = Follower
        fields = ["type", "summary", "actor", "object", "approved"]

    def create(self, validated_data):
        follow, created = Follower.objects.update_or_create(defaults=validated_data)
        return follow, created
    
    def create_relations(self, author_id, foreign_author_id):
    
        try:
            from_author_obj = author_serializer.get_author_by_id(foreign_author_id)
        except ValidationError:
            return None

        try:
            to_author_obj = author_serializer.get_author_by_id(author_id)
        except ValidationError:
            return None
        
        try:
            relation = self.get_relation_by_ids(author_id, foreign_author_id)
        except ValidationError:
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
        try:
            follower = Follower.objects.get(from_author=foreign_author_id, to_author=author_id)
        except Follower.DoesNotExist:
            raise ValidationError("Follower does not exist")

        return follower
    
    def follower_exists(self, author_id, foreign_author_id):
        try:
            follower = self.get_relation_by_ids(author_id, foreign_author_id)
        except ValidationError:
            return False
        return True

class AllFollowerSerializer(serializers.Serializer):
    type = serializers.CharField(default="followers" , max_length=10, read_only=True, required=False)
    page = serializers.IntegerField(allow_null=True, required=False)
    size = serializers.IntegerField(allow_null=True, required=False)
    items = AuthorSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['page'] is None:
            data.pop('page')
        if data['size'] is None:
            data.pop('size')
        return data