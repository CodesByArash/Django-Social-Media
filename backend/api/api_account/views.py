from django.shortcuts import render
from django.http import JsonResponse


from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from .serializers import *


class ChangePasswordView(generics.UpdateAPIView):

    # queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user
    