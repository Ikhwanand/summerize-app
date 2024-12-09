from django.contrib import admin
from .models import VideoSummary
# Register your models here.
class VideoSummaryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('title', 'summary', 'video_url')
    readonly_fields = ('created_at',)

admin.site.register(VideoSummary, VideoSummaryAdmin)