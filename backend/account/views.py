from django.contrib.auth import authenticate , login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as SigninView
from .forms import UserRegisterForm , UserLoginForm
# Create your views here.

class SignUpView(CreateView):
    template_name = 'account/signup.html'
    success_url = reverse_lazy('core.home')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"
    
    
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
    success_url = reverse_lazy('core.home')
    form_class = UserLoginForm
    success_message = "successfully logged in"
