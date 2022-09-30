from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Post
# Create your views here.


@login_required
def home(request):
    return render(request, 'socialmedia/index.html')


def post(request,pk):
    post = Post.objects.filter(id=pk)
    context ={'posts': post}
    return render(request ,'socialmedia/index.html' ,context=context)