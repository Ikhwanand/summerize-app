from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoSummaryViewSet

router = DefaultRouter()
router.register(r"summaries", VideoSummaryViewSet, basename='video-summary')

urlpatterns = [
    path('', include(router.urls)),
]
