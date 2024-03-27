from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
from django.utils.translation import gettext_lazy as _


# class CustomUserManager(BaseUserManager):
#     def _create_user(self, name, email, password, **extra_fields):
#         if not email:
#             raise ValueError("you have not provided a valid e-mail address")
        
#         email = self.normalize_email(email)
#         user = self.model(email=email, name=name, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)

#         return user
#     def create_user(self, name=None, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(name, email, password, **extra_fields)

#     def create_superuser(self, name=None, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self._create_user(name, email, password, **extra_fields)


class User(AbstractUser):  
    id                = models.UUIDField(primary_key = True, default= uuid.uuid4, editable = False)
    username          = models.CharField(max_length = 50, blank = False, null = False, unique = True)  
    email             = models.EmailField(_('Email Address'), max_length=50, unique=True)
    is_email_verified = models.BooleanField(default=False)
    first_name        = models.CharField(default = "null", max_length=500, blank=True, null=True)
    last_name         = models.CharField(default = "null", max_length=500, blank=True, null=True)
    is_staff          = models.BooleanField(default=False, verbose_name='staff')
    bio               = models.TextField(blank=True, max_length=500)
    profile_img       = models.ImageField(upload_to='profile_images',default='/profile_images/default.png')
    followers         = models.IntegerField(default=0)
    followings        = models.IntegerField(default=0)
    posts             = models.IntegerField(default=0)
    
    follows         = models.ManyToManyField('self', related_name='followed_by', blank= True, symmetrical=False)

    # objects = CustomUserManager()

    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    