from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderDetailViewSet

urlpatterns = [
    path('create/', OrderDetailViewSet.as_view({'post': 'create_orderdetails'}), name='create_orderdetails'),
]