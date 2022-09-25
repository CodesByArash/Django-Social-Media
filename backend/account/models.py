from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    bio = models.TextField(blank=True, max_length=500)
    profile_img = models.ImageField(upload_to='profile_images',default='/profile_images/default.png')
    
    
