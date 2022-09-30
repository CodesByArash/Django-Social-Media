from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

# admin.site.register(User, UserAdmin)

UserAdmin.fieldsets[2][1]['fields']=(
    'posts',
    'followers',
    'followings',
    'bio',)

# UserAdmin.list_display +=('is_author',)

admin.site.register(User,UserAdmin)