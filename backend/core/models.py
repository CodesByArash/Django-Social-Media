from datetime import datetime
from uuid import uuid4
from django.db import models
from account.models import *
# Create your models here.

class Follow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='followed')
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    image = models.ImageField(upload_to='post_images')
    user  = models.ForeignKey(User,on_delete=models.CASCADE)
    caption = models.TextField()
    creation_time = models.DateTimeField(default=datetime.now)
    like_no       = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username
    

class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
    