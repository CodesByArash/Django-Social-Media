from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostUploadForm, SearchForm
from .models import Post, Comment
from account.models import User

@login_required
def home(request):
    if request.method == 'POST':
        form = PostUploadForm(request.POST, request.FILES)
        if form.is_valid():
            Post.objects.create(
                user=request.user,
                image=form.cleaned_data['image'],
                caption=form.cleaned_data['caption']
            )
            messages.success(request, 'Post created successfully!')
            return redirect('home')
    else:
        form = PostUploadForm()

    posts = Post.objects.all().order_by('-creation_time')
    posts_with_likes = [(post, post.is_liked_by(request.user)) for post in posts]

    context = {'posts': posts_with_likes, 'form': form}
    return render(request, 'socialmedia/index.html', context=context)


@login_required
def post(request, pk):
    post = get_object_or_404(Post, id=pk)
    posts_with_likes = [(post, post.is_liked_by(request.user))]
    context = {'posts': posts_with_likes}
    return render(request, 'socialmedia/post-detail.html', context=context)


@login_required
def like(request):
    post_id = request.GET.get('post_id')
    next_url = request.GET.get('next', '/')

    if post_id:
        post = get_object_or_404(Post, id=post_id)
        post.toggle_like(request.user)

    return HttpResponseRedirect(next_url)


@login_required
def deletepost(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.delete_post(request.user):
        messages.success(request, 'Post deleted successfully!')
    else:
        messages.error(request, 'You can only delete your own posts!')

    return redirect('home')


@login_required
def search(request):
    search_form = SearchForm(request.GET)
    users = None
    if search_form.is_valid():
        query = search_form.cleaned_data['search']

        users = User.objects.search_users(query, exclude_user=request.user)

    context = {'query': users if users and users.exists() else None}
    return render(request, 'socialmedia/search.html', context=context)


@login_required
def post_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(post=post, user=request.user, text=text)
            messages.success(request, 'Comment added!')
            return redirect('post', pk=post_id)

    comments = post.comments.all().order_by('creation_time')
    context = {'post': post, 'comments': comments}
    return render(request, 'socialmedia/post-comments.html', context=context)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id
    if comment.user == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted!')
    else:
        messages.error(request, 'You can only delete your own comments!')
    return redirect('post', pk=post_id)


@login_required
def follow_toggle(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    if User.objects.is_following(request.user, target_user):
        User.objects.unfollow_user(request.user, target_user)
    else:
        User.objects.follow_user(request.user, target_user)
    next_url = request.GET.get('next', '/')
    return HttpResponseRedirect(next_url)
