from rest_framework import serializers
from .models import VideoSummary

class VideoURLSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)

class VideoSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoSummary
        fields = ['id', 'video_url', 'title', 'summary', 'thumbnail_url', 'duration', 'created_at']
        read_only_fields = ['created_at']