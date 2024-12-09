from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from .models import VideoSummary
from .serializers import VideoSummarySerializer, VideoURLSerializer
from .ai_utils import get_video_info, generate_summary
import logging
logger = logging.getLogger(__name__)

class VideoSummaryViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return VideoSummary.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def recent(self):
        """Get summaries from the last 7 days"""
        last_week = timezone.now() - timedelta(days=7)
        recent_summaries = self.get_queryset().filter(created_at__gte=last_week)
        serializer = self.get_serializer(recent_summaries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self):
        """Get user's summary statistics"""
        queryset = self.get_queryset()
        total_summaries = queryset.count()
        recent_summaries = queryset.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        return Response({
            'total_summaries': total_summaries,
            'recent_summaries': recent_summaries,
            'last_summary': queryset.first().created_at if queryset.exists() else None
        })

    @action(detail=False, methods=['post'])
    def summarize(self, request):
        serializer = VideoURLSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Get video info
                video_info = get_video_info(serializer.validated_data['url'])
                
                # Generate summary from video description
                summary = generate_summary(video_info['description'])
                
                # Create or update summary
                summary_obj, created = VideoSummary.objects.update_or_create(
                    user=request.user,
                    video_url=serializer.validated_data['url'],
                    defaults={
                        'title': video_info['title'],
                        'summary': summary,
                        'thumbnail_url': video_info['thumbnail_url'],
                        'duration': video_info['duration']
                    }
                )
                
                return Response(
                    VideoSummarySerializer(summary_obj).data,
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                # Log the full exception details
                logger.error(f"Summarization Error: {str(e)}", exc_info=True)
                
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        # Log validation errors
        logger.error(f"Serializer Validation Error: {serializer.errors}")
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['delete'])
    def clear_history(self, request):
        """Clear all user's summaries"""
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)