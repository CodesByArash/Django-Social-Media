from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
import uuid

class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError(_("The Username must be set"))
        if not email:
            raise ValueError(_("The Email must be set"))

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(username, email, password, **extra_fields)

    def search_users(self, query, exclude_user=None):
        qs = self.get_queryset().filter(username__icontains=query)
        if exclude_user:
            qs = qs.exclude(id=exclude_user.id)
        return qs

class User(AbstractUser):  
    id                = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username          = models.CharField(max_length=50, blank=False, null=False, unique=True)  
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
    follows           = models.ManyToManyField('self', related_name='followed_by', blank=True, symmetrical=False)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return self.username

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()
    
    def get_short_name(self):
        return self.first_name

    def follow(self, other_user):
        if self != other_user and not self.is_following(other_user):
            self.follows.add(other_user)
            self.save()
            return True
        return False

    def unfollow(self, other_user):
        if self.is_following(other_user):
            self.follows.remove(other_user)
            self.save()
            return True
        return False

    def is_following(self, other_user):
        return self.follows.filter(id=other_user.id).exists()

    def toggle_follow(self, other_user):
        if self.is_following(other_user):
            return self.unfollow(other_user)
        else:
            return self.follow(other_user)

    @property
    def posts_count(self):
        return self.post_set.count()

    @property
    def followers_count(self):
        return self.followed_by.count()

    @property
    def followings_count(self):
        return self.follows.count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

