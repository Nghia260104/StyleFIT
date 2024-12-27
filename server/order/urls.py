from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

urlpatterns = [
    path('create/', OrderViewSet.as_view({'post': 'create'}), name='create_order'),
    path('update/', OrderViewSet.as_view({'post': 'update_status'}), name='update_order'),
]