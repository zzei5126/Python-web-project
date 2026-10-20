from rest_framework import serializers
from .models import Entry


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ["id", "name", "message", "created_at"]
        read_only_fields = ["id", "created_at"]


class SenderSerializer(serializers.Serializer):
    name = serializers.CharField()
    count = serializers.IntegerField()


class StatsSerializer(serializers.Serializer):
    total_entries = serializers.IntegerField()
    total_senders = serializers.IntegerField()
    top_senders = SenderSerializer(many=True)
    senders = SenderSerializer(many=True)
