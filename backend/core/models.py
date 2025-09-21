from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from account.models import User



class Post(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid4)
    image         = models.ImageField(
        upload_to='post_images',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        help_text='Upload an image (JPG, JPEG, PNG, GIF only)'
    )
    user          = models.ForeignKey(User,on_delete=models.CASCADE)
    caption       = models.TextField(blank=True, max_length=2000, help_text='Write a caption for your post')
    creation_time = models.DateTimeField(default=timezone.now)
    liked_by      = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.caption[:50]}{"..." if len(self.caption) > 50 else ""}"
    
    def get_likes_count(self):

        return self.liked_by.count()
    
    def is_liked_by(self, user):

        return self.liked_by.filter(id=user.id).exists()
    
    def like_post(self, user):

        if not self.is_liked_by(user):
            self.liked_by.add(user)
            self.save()
            return True
        return False
    
    def unlike_post(self, user):

        if self.is_liked_by(user):
            self.liked_by.remove(user)
            self.save()
            return True
        return False
    
    def toggle_like(self, user):

        if self.is_liked_by(user):
            return self.unlike_post(user)
        else:
            return self.like_post(user)
    
    def delete_post(self, user):

        if self.user == user:
            self.delete()
            return True
        return False
    
    @classmethod
    def create_post(cls, user, image, caption=''):
        """Create a new post"""
        post = cls.objects.create(
            user=user,
            image=image,
            caption=caption
        )
        return post
    
    @classmethod
    def get_user_posts(cls, user):

        return cls.objects.filter(user=user).order_by('-creation_time')

    
    @classmethod
    def get_feed_posts(cls, user):

        following_users = user.follows.all()
        following_users = following_users.union([user])  # Include own posts
        return cls.objects.filter(user__in=following_users).order_by('-creation_time')
    
    def save(self, *args, **kwargs):

        self.like_no = self.get_likes_count()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-creation_time']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comment(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid4)
    post          = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    text          = models.TextField(max_length=1000)
    creation_time = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} commented on {self.post.user.username}'s post"
    
    class Meta:
        ordering = ['creation_time']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

