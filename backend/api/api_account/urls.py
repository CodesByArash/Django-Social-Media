from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/',UserSignUpView.as_view(), name='api_signup'),
    path('',UserProfileListView.as_view(), name='api_user_list'),
    path('<str:pk>',UserProfileDetailView.as_view(), name='api_user_detail'),
    path('update/',UpdateProfileView.as_view(), name='api_update'),
    path('changepassword/', ChangePasswordView.as_view(), name='api_change_password'),
    
]

