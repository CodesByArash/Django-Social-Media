from django.shortcuts import render
from django.http import JsonResponse


from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, response, status, response

from .serializers import *


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.validated_data)
            user.save()

            return response.Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)
        

