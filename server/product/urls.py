from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

urlpatterns = [
    path('add/', ProductViewSet.as_view({'post': 'add_product'}), name='add_product'),
    path('remove/', ProductViewSet.as_view({'post': 'remove_product'}), name='remove_product'),
    path('get-rating/<str:pk>', ProductViewSet.as_view({'get': 'get_rating'}), name='get_rating'),
]