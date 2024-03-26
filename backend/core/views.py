from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
        is_liked = post.liked_by.filter(id=request.user.id).first()

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
        is_liked = post.liked_by.filter(id=request.user.id).first()
        if is_liked is None:
            like_list.append(False)
        else:
            like_list.append(True)
    posts = zip(posts,like_list)
    context ={'posts': posts}
    return render(request ,'socialmedia/post-detail.html' ,context=context)


@login_required
def like(request):
    user = request.user
    post_id = request.GET.get('post_id')
    post    = get_object_or_404(Post,id=post_id)
    liked   = post.liked_by.filter(id=user.id).first()
    next = request.GET.get('next')
    if liked is None:
        post.liked_by.add(user)
        post.like_no += 1
        post.save()
    else:
        post.liked_by.remove(user)
        post.like_no -= 1
        post.save()
    
    return HttpResponseRedirect(next)
    

@login_required
def deletepost(request,pk):
    post    = get_object_or_404(Post,pk=pk)
    user    = request.user
    if request.user == post.user:
        user.posts -= 1
        user.save()
        post.delete()
        return redirect('home')

    return redirect('home')

@login_required
def search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        username = search_form.cleaned_data['search']
        query   = User.objects.filter(username__icontains=username).exclude(pk=request.user.id)
        if len(query)==0:
            query=None
        context = {'query':query,}
    else:
        context = {'query': None}
    
    return render(request ,'socialmedia/search.html' ,context=context)

