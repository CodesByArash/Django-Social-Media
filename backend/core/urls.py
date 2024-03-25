from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('post/<slug:pk>',post, name='post'),
    path('like/',like, name='like'),
    path('post/<slug:pk>/delete', deletepost, name='delete'),
    path('search/', search, name='search'),
]