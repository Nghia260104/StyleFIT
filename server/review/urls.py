from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet

urlpatterns = [
    path('create/', ReviewViewSet.as_view({'post': 'create_review'}), name='create_review'),
]