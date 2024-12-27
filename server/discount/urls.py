from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DiscountViewSet

urlpatterns = [
    path('create/', DiscountViewSet.as_view({'post': 'create_discount'}), name='create_discount'),
]