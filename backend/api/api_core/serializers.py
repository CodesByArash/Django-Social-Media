from rest_framework import serializers
from core.models import *


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = {'image', 'user', 'caption', 'creation_time', 'like_no'}
        