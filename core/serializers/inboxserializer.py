# Local libraries
from .. models import Inbox

# Third-party libraries
from rest_framework import serializers
       

class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        fields = "__all__"
