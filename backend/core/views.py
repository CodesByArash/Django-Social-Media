from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Post
# Create your views here.


@login_required
def home(request):
    if request.method == "POST":
        image = request.FILES.get('img')
        user  = request.user
        caption = request.POST.get('caption')
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('home')

    posts = Post.objects.all().order_by('-creation_time')
    context ={'posts': posts}
    return render(request, 'socialmedia/index.html',context=context)


@login_required
def post(request,pk):
    post = Post.objects.filter(id=pk)
    context ={'posts': post}
    return render(request ,'socialmedia/post-detail.html' ,context=context)


@login_required
def like(request):
    pass