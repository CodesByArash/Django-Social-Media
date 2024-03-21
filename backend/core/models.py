from datetime import datetime
from uuid import uuid4
from django.db import models
from account.models import *



class Post(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid4)
    image         = models.ImageField(upload_to='post_images')
    user          = models.ForeignKey(User,on_delete=models.CASCADE)
    caption       = models.TextField()
    creation_time = models.DateTimeField(default=datetime.now)
    like_no       = models.IntegerField(default=0)
    liked_by      = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    def __str__(self):
        return self.user.username