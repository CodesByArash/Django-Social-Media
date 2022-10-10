from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm,UserChangeForm
from .models import Post
from django import forms



# class UserRegisterForm(UserCreationForm):
#     caption = forms.CharField(widget= forms.EmailInput
#                            (attrs={'placeholder':'Email*'}))
    
#     image = forms.CharField(widget= forms.ImageField
#                                (attrs={'placeholder':'Username*'}))
    
    
#     class Meta:
#         model = Post
#         fields = ['image','caption','user']
        
        