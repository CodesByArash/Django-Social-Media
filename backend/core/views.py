from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import *
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
    like_list = []
    for post in posts:
        is_liked = Like.objects.filter(user=request.user, post= post).first()
        if is_liked is None:
            like_list.append(False)
        else:
            like_list.append(True)
    posts = zip(posts,like_list)
    
    print(posts)
    context ={'posts': posts}
    return render(request, 'socialmedia/index.html',context=context)


@login_required
def post(request,pk):
    posts = get_list_or_404(Post,id=pk)
    like_list = []
    for post in posts:
        is_liked = Like.objects.filter(user=request.user, post= post).first()
        if is_liked is None:
            like_list.append(False)
        else:
            like_list.append(True)
    posts = zip(posts,like_list)
    print(posts)
    context ={'posts': posts}
    return render(request ,'socialmedia/post-detail.html' ,context=context)


@login_required
def like(request):
    user = request.user
    post_id = request.GET.get('post_id')
    post    = get_object_or_404(Post,id=post_id)
    liked = Like.objects.filter(user=user,post=post).first()
    
    if liked is None:
        like = Like.objects.create(post=post,user=user)
        like.save()
        post.like_no += 1
        post.save()
        return redirect('home')
    else:
        liked.delete()
        post.like_no -= 1
        post.save()
        return redirect('home')
    

@login_required
def follow(request):
    pass