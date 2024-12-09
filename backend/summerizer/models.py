from django.db import models
from django.conf import settings

# Create your models here.
class VideoSummary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_url = models.URLField()
    title = models.CharField(max_length=255)
    summary = models.TextField()
    thumbnail_url = models.URLField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Video Summaries'
        
    def __str__(self):
        return f"{self.title} - {self.user.email}"
    