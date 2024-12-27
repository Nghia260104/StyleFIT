from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

urlpatterns = [
    path('add/', ProductViewSet.as_view({'post': 'add_product'}), name='add_product'),
    path('remove/', ProductViewSet.as_view({'post': 'remove_product'}), name='remove_product'),
    # path('get-rating/<int:pk>', ProductViewSet.as_view({'get': 'get_rating'}), name='get_rating'),
    path('get/seller/<int:pk>/', ProductViewSet.as_view({'get': 'get_products_seller'}), name='get_products_seller'),
    path('get/', ProductViewSet.as_view({'get': 'get_products'}), name='get_products'),
    path('get/<int:pk>/', ProductViewSet.as_view({'get': 'get_product'}), name='get_product'),
]