from rest_framework import serializers
from apps.outdoor.models import OutdoorActivity


class NewEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutdoorActivity
        fields = "__all__"