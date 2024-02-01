from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    # path('', home, name='home'),
    path('', index.as_view(), name='home'),
    path('post/<slug:pk>',post, name='post'),
    path('like/',like, name='like'),
]