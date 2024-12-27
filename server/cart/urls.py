from django.urls import path
from .views import CartViewSet

urlpatterns = [
    path('add/', CartViewSet.as_view({'post': 'add'}), name='add'),
    path('update/', CartViewSet.as_view({'post': 'update'}), name='update'),
]