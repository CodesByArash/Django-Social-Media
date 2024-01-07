from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DeleteView
from .forms import *
from .models import *
from account.models import *

# Create your views here.


class index(LoginRequiredMixin,ListView):
    # form_class = PostUploadForm
    
    def post(self, request):
        # form = self.form_class(request.POST, request.FILES)
        
        # if form.is_valid():
        #     form.save(user=self.request.user)
        # else:
        #     print(form.errors)
        #     print("arash")

        
        # upload post without forms
        image = request.FILES.get('img')
        user  = request.user
        caption = request.POST.get('caption')
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        user.posts+=1
        user.save()
        
        
        posts = Post.objects.all().order_by('-creation_time')
        like_list = []
        for post in posts:
            is_liked = Like.objects.filter(user=request.user, post= post).first()
            if is_liked is None:
                like_list.append(False)
            else:
                like_list.append(True)
        posts = zip(posts,like_list)
        
        
        context ={'posts': posts}
        # context['form']=form
        return render(request, 'socialmedia/index.html',context=context)
    
    def get(self,request):
        # form = PostUploadForm()
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
        context = {'posts': posts}
        # context['form'] = form
        return render(request, 'socialmedia/index.html',context=context)

# @login_required
# def home(request):
#     if request.method == "POST":
#         image = request.FILES.get('img')
#         user  = request.user
#         caption = request.POST.get('caption')
#         new_post = Post.objects.create(user=user, image=image, caption=caption)
#         new_post.save()
#         user.posts+=1
#         user.save()
#         return redirect('home')

#     posts = Post.objects.all().order_by('-creation_time')
#     like_list = []
#     for post in posts:
#         is_liked = Like.objects.filter(user=request.user, post= post).first()
#         if is_liked is None:
#             like_list.append(False)
#         else:
#             like_list.append(True)
#     posts = zip(posts,like_list)
    
#     print(posts)
#     context ={'posts': posts}
#     return render(request, 'socialmedia/index.html',context=context)



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
    


@login_required
def follow(request):
    follower = request.user
    username = request.GET.get('username')
    next = request.GET.get('next')
    followed = get_object_or_404(User,username=username)
    follows  = Follow.objects.filter(user=followed,follower=follower).first()
    
    if follows is None:
        follow_relation = Follow.objects.create(user=followed, follower=follower)
        follow_relation.save()
        follower.followings += 1
        follower.save()
        followed.followers  += 1
        followed.save()
    else:
        follows.delete()
        follower.followings -= 1
        follower.save()
        followed.followers  -= 1
        followed.save()
        
    return HttpResponseRedirect(next)
    
    
    
    