from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

urlpatterns = [
    path('add/', ProductViewSet.as_view({'post': 'add_product'}), name='add_product'),
]