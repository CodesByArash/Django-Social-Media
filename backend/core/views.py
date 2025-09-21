from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
from account.models import *


from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .repositories import PostRepository, UserRepository
from account.models import User


@login_required
def home(request):
    if request.method == 'POST':
        form = PostUploadForm(request.POST, request.FILES)
        if form.is_valid():
            PostRepository.create_post(
                user=request.user,
                image=form.cleaned_data['image'],
                caption=form.cleaned_data['caption']
            )
            messages.success(request, 'Post created successfully!')
            return redirect('home')
    else:
        form = PostUploadForm()

    posts = PostRepository.get_all_posts()
    posts_with_likes = PostRepository.get_posts_with_like_status(posts, request.user)
    
    context = {
        'posts': posts_with_likes, 
        'form': form
    }
    return render(request, 'socialmedia/index.html', context=context)


@login_required
def post(request, pk):
    post = PostRepository.get_post_by_id(pk)
    if not post:
        return redirect('home')
    
    posts_with_likes = PostRepository.get_posts_with_like_status([post], request.user)
    context = {'posts': posts_with_likes}
    return render(request, 'socialmedia/post-detail.html', context=context)


@login_required
def like(request):
    post_id = request.GET.get('post_id')
    next_url = request.GET.get('next')
    
    if post_id:
        PostRepository.toggle_like(post_id, request.user)
    
    return HttpResponseRedirect(next_url)
    

@login_required
def deletepost(request, pk):
    success = PostRepository.delete_post(pk, request.user)
    if success:
        messages.success(request, 'Post deleted successfully!')
    else:
        messages.error(request, 'You can only delete your own posts!')
    
    return redirect('home')

@login_required
def search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data['search']
        users = UserRepository.search_users(query, exclude_user=request.user)
        context = {'query': users if users.exists() else None}
    else:
        context = {'query': None}
    
    return render(request, 'socialmedia/search.html', context=context)

