from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AccountViewSet

urlpatterns = [
    path('register/', AccountViewSet.as_view({'post': 'register'}), name='register'),
    path('login/', AccountViewSet.as_view({'post': 'login'}), name='login'),
]