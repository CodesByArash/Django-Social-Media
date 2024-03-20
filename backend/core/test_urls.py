from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import *


class test_follow_url_resolves(SimpleTestCase):
    def test_list_url_is_resolved(self):
        url = reverse('follow')
        self.assertEquals(resolve(url).func, follow)

    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func.view_class, SignUpView)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_profile_url_resolves(self):
        url = reverse('profile', args=['some_str'])
        self.assertEquals(resolve(url).func.view_class, ProfileView)

    def test_settings_url_resolves(self):
        url = reverse('settings')
        self.assertEquals(resolve(url).func.view_class, SettingsView)

    def test_password_url_resolves(self):
        url = reverse('password')
        self.assertEquals(resolve(url).func, PasswordChangeView)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, LogoutView)

    