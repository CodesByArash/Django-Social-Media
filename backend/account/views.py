from django.contrib.auth import authenticate , login
from django.contrib import messages
from .models import User
from core.models import *
from core.models import Post
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView , DetailView ,UpdateView
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as SigninView
from .forms import UserRegisterForm, UserLoginForm, UserSettingsForm, MyPasswordChangeForm


class SignUpView(CreateView):
    template_name = 'account/signup.html'
    success_url = reverse_lazy('home')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        
        return super().dispatch(request, *args, **kwargs)
        
    
    def form_valid(self, form):
        to_return = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return to_return


class LoginView(SigninView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('core:home')
    form_class = UserLoginForm
    success_message = "successfully logged in"
    

class ProfileView(LoginRequiredMixin,DetailView):
    model = User
    template_name: str = 'account/profile.html'
    
    def get_object(self):
        username=self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return user    
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['post'] = Post.objects.filter(user=context_data['object'])
        follow_relation = self.request.user.follows.filter(id=context_data['object']).first()
        if(follow_relation is None):
            context_data['unfollow'] = False
        else:
            context_data['unfollow'] = True

        return context_data


class SettingsView(LoginRequiredMixin,UpdateView):
    model = User
    template_name = 'account/settings.html'
    success_url = reverse_lazy('settings')
    fields = ['username', 'email', 'first_name', 'last_name', 'bio', ]
    form = UserSettingsForm
    
    def get_object(self):
            return self.request.user


@login_required
def PasswordChangeView(request):
    if request.method == 'POST':
        password_form = MyPasswordChangeForm(request.user,request.POST)
        if password_form.is_valid():
            user=password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request,'Your password wa successfully updated')
            return redirect('settings')
        else:
            pass
            # messages.error(request,'Please correct  the error below.')
    else:
        password_form = MyPasswordChangeForm(request.user)
        
    return render(request, 'account/password.html', {
        'form':password_form
    })


@login_required        
def LogoutView(request):
    logout(request)
    return redirect('login')


@login_required
def follow(request):
    follower = request.user
    username = request.GET.get('username')
    next = request.GET.get('next')
    followed = get_object_or_404(User,username=username)
    follows  = follower.follows.filter(id=followed.id).first()
    
    if follows is None:
        follows = follower.follows.add(id=followed.id)
        follower.followings += 1
        follower.save()
        followed.followers  += 1
        followed.save()
    else:
        follower.follows.remove(followed)
        follower.followings -= 1
        follower.save()
        followed.followers  -= 1
        followed.save()
        
    return HttpResponseRedirect(next)

 