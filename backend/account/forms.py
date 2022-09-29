from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm,UserChangeForm
from account.models import User
from django import forms
from django.utils.safestring import mark_safe

from django.contrib.auth.forms import PasswordChangeForm

# Create your tests here.
class UserRegisterForm(UserCreationForm):
    email = forms.CharField(widget= forms.EmailInput
                           (attrs={'placeholder':'Email*'}))
    
    username = forms.CharField(widget= forms.TextInput
                                 (attrs={'placeholder':'Username*'})
                                 ,help_text=mark_safe("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."))
    
    first_name = forms.CharField(required = False,widget= forms.TextInput
                                 (attrs={'placeholder':'First Name'}))
    
    last_name  = forms.CharField(required = False,widget= forms.TextInput
                           (attrs={'placeholder':'Last Name'}))
    
    password1  = forms.CharField(widget=forms.PasswordInput
                                 (attrs={'placeholder':'Password*'}),help_text=mark_safe('Your password can’t be too similar to your other personal information.<br/>Your password must contain at least 8 characters.<br/>Your password can’t be a commonly used password.<br/>Your password can’t be entirely numeric.'))
    
    password2  = forms.CharField(widget=forms.PasswordInput
                                 (attrs={'placeholder':'Password Confirmation*'}),help_text=mark_safe("Enter the same password as before, for verification."))
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']





class UserSettingsForm(UserChangeForm):
    email = forms.CharField(widget= forms.EmailInput
                           (attrs={'placeholder':'Email*'}))
    
    username = forms.CharField(widget= forms.TextInput
                                 (attrs={'placeholder':'Username*'})
                                 ,help_text=mark_safe("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."))
    
    first_name = forms.CharField(required = False,widget= forms.TextInput
                                 (attrs={'placeholder':'First Name'}))
    
    last_name  = forms.CharField(required = False,widget= forms.TextInput
                           (attrs={'placeholder':'Last Name'}))
    
    bio  = forms.CharField(required = False,widget= forms.TextInput
                           (attrs={'placeholder':'Bio'}))
    
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', ]



class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput
                                 (attrs={'placeholder':'Old Password*'}))
    new_password1 =forms.CharField(widget=forms.PasswordInput
                                 (attrs={'placeholder':'New Password*'})
                                 ,help_text=mark_safe('Your password can’t be too similar to your other personal information.<br/>Your password must contain at least 8 characters.<br/>Your password can’t be a commonly used password.<br/>Your password can’t be entirely numeric.'))
    new_password2 =forms.CharField(widget=forms.PasswordInput
                                 (attrs={'placeholder':'Confirm Password*'}))
    



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget= forms.TextInput
                                 (attrs={'placeholder':'Username*'})
                                 ,help_text=mark_safe("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."))
    
    password  = forms.CharField(widget=forms.PasswordInput
                                 (attrs={'placeholder':'Password*'}),help_text=mark_safe('Your password can’t be too similar to your other personal information.<br/>Your password must contain at least 8 characters.<br/>Your password can’t be a commonly used password.<br/>Your password can’t be entirely numeric.'))
    