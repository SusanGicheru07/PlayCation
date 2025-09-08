from rest_framework import serializers


class NewEventSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    category = serializers.CharField(max_length=100)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    created_at = serializers.DateTimeField()