from django.shortcuts import render
from django.http import JsonResponse


from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, response, status, response, views
from rest_framework import mixins

from .serializers import *



class ChangePasswordView(generics.GenericAPIView):
    serializer_class   = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.validated_data)
            user.save()

            return response.Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)
                
        return response.Response({'detail': 'Password Update failed', 'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    


class UpdateProfileView(generics.UpdateAPIView):
    serializer_class   = UserProfileUpdateSerializer
    permission_classes = (IsAuthenticated,)
    

    def get_object(self):
        return self.request.user




class UserProfileDetailView(generics.RetrieveAPIView):
    queryset           = User.objects.all()
    serializer_class   = UserProfileSerializer
    permission_classes = (AllowAny,)



class UserProfileListView(generics.ListAPIView):
    queryset           = User.objects.all()
    serializer_class   = UserProfileSerializer
    permission_classes = (AllowAny,)



class UserSignUpView(generics.GenericAPIView):
    serializer_class   = UserProfileCreateSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            data = request.data
            serializer = UserProfileCreateSerializer(data = data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                
                return response.Response({
                    'status':200,
                    'message':'registered succesfully check email',
                    'data':serializer.data,
                })
            
            return response.Response({
                'status':400,
                'message':'something went wrong',
                'data': serializer.errors
            })
        
        except Exception as e:
            return response.Response({'message': f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        

