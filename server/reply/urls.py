from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ReplyViewSet

urlpatterns = [
    path('create/', ReplyViewSet.as_view({'post': 'create_reply'}), name='create_reply'),
    path('get/<int:pk>/', ReplyViewSet.as_view({'get': 'get_replies'}), name='get_replies'),
]