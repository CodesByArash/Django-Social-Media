from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DeleteView
from django.views import View
from .forms import *
from .models import *
from account.models import *


@login_required
def home(request):
    if request.method == 'POST':
        form = PostUploadForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.user=user
            post.save()
            user.posts+=1
            user.save()
    else:
        form = PostUploadForm()

    posts = Post.objects.all().order_by('-creation_time')
    like_list = []
    for post in posts:
        is_liked = Like.objects.filter(user=request.user, post= post).first()
        if is_liked is None:
            like_list.append(False)
        else:
            like_list.append(True)
    posts = zip(posts,like_list)
    context = {'posts': posts, 'form':form}
        
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
    next = request.GET.get('next')

    if liked is None:
        like = Like.objects.create(post=post,user=user)
        like.save()
        post.like_no += 1
        post.save()
    else:
        liked.delete()
        post.like_no -= 1
        post.save()
    
    return HttpResponseRedirect(next)
    


@login_required
def deletepost(request):
    post_id = request.GET.get('post_id')
    post    = get_object_or_404(Post,id=post_id)
    if request.user == post.user:
        request.user.posts -= 1
        post.delete()
        return HttpResponseRedirect('home')

    return redirect('home')
    



    
    
    
    