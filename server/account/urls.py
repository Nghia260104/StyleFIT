from django.urls import path
from .views import AccountViewSet

urlpatterns = [
    path('register/', AccountViewSet.as_view({'post': 'register'}), name='register'),
    path('login/', AccountViewSet.as_view({'post': 'login'}), name='login'),
    path('change-password/', AccountViewSet.as_view({'post': 'change_password'}), name='change-password'),
    path('update-profile-info/', AccountViewSet.as_view({'post': 'update_profile_info'}), name='update-profile-info'),
]