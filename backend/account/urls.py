from cProfile import Profile
from django.contrib import admin
from django.urls import path
from .views import SignUpView , LoginView ,ProfileView

urlpatterns = [
    path('signup/',SignUpView.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('profile/<str:username>/',ProfileView.as_view(), name="profile")
]