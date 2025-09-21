from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
import uuid


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
    first_name        = models.CharField(max_length=150, blank=True, null=True)
    last_name         = models.CharField(max_length=150, blank=True, null=True)
    is_staff          = models.BooleanField(default=False, verbose_name='staff')
    bio               = models.TextField(blank=True, max_length=500, help_text='Tell us about yourself')
    profile_img       = models.ImageField(
        upload_to='profile_images',
        default='profile_images/default.png',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        help_text='Upload a profile picture (JPG, JPEG, PNG, GIF only)'
    )
    followers         = models.IntegerField(default=0)
    followings        = models.IntegerField(default=0)
    posts             = models.IntegerField(default=0)
    
    follows         = models.ManyToManyField('self', related_name='followed_by', blank= True, symmetrical=False)

    # objects = CustomUserManager()

    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return self.username

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
    
    def get_followers_count(self):
        """Return the actual count of followers from the relationship."""
        return self.followed_by.count()
    
    def get_following_count(self):
        """Return the actual count of following from the relationship."""
        return self.follows.count()
    
    def get_posts_count(self):
        """Return the actual count of posts."""
        return self.post_set.count()
    
    def follow_user(self, user_to_follow):
        """Follow another user"""
        if self != user_to_follow and not self.is_following(user_to_follow):
            self.follows.add(user_to_follow)
            self.save()
            return True
        return False
    
    def unfollow_user(self, user_to_unfollow):
        """Unfollow another user"""
        if self.is_following(user_to_unfollow):
            self.follows.remove(user_to_unfollow)
            self.save()
            return True
        return False
    
    def is_following(self, user):
        """Check if this user is following another user"""
        return self.follows.filter(id=user.id).exists()
    
    def toggle_follow(self, user):
        """Toggle follow/unfollow status"""
        if self.is_following(user):
            return self.unfollow_user(user)
        else:
            return self.follow_user(user)
    
    def search_users(self, query):
        """Search for users by username"""
        return User.objects.filter(
            username__icontains=query
        ).exclude(id=self.id)
    
    def save(self, *args, **kwargs):
        # Update counters with actual counts
        self.followers = self.get_followers_count()
        self.followings = self.get_following_count()
        self.posts = self.get_posts_count()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    