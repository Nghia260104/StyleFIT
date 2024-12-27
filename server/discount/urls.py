from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DiscountViewSet

urlpatterns = [
    path('create/', DiscountViewSet.as_view({'post': 'create_discount'}), name='create_discount'),
    path('edit/<int:pk>/', DiscountViewSet.as_view({'put': 'edit_discount'}), name='edit_discount'),
]