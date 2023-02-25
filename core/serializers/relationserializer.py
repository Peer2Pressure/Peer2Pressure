# Local libraries
from .. models import *

# Third-party libraries
from rest_framework import serializers
from varname import nameof        

class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = "__all__"

    def create_relations(self, from_author, to_author):

        try:
            from_author_obj = Author.objects.get(id=from_author)
        except Author.DoesNotExist:
            raise ValueError("From Author does not exist")
        
        try:
            to_author_obj = Author.objects.get(id=to_author)
        except Author.DoesNotExist:
            raise ValueError("To Author does not exist")
        
        defaults = {
            nameof(Relation.from_author): from_author_obj,
            nameof(Relation.to_author): to_author_obj
        }

        relation_obj= Relation.objects.create(**defaults)

        return relation_obj.id
