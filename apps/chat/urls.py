from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, MessageViewSet, AudioViewSet, VideoViewSet

router = DefaultRouter()
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'audio', AudioViewSet, basename='audio')
router.register(r'video', VideoViewSet, basename='video')

urlpatterns = [
    path('', include(router.urls)),
]
