from django.test import TestCase
from .forms import *

class TestForms(TestCase):
    
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user=User.objects.create_user(**self.credentials)
    
    def test_UserLoginForm_valid_data(self):
        form = UserLoginForm(data={
            'username':'testuser',
            'password':'secret',
        })

        self.assertTrue(form.is_valid())

    def test_UserLoginForm_no_data(self):
        form = UserLoginForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_UserRegisterForm_valid_data(self):
        form = UserRegisterForm(data={
            'email':'test@gmail.com',
            'username':'test',
            'password1':'testpassword',
            'password2':'testpassword',
            'first_name':'test',
            'last_name':'test',
        })
        self.assertTrue(form.is_valid())

    def test_UserRegisterForm_no_data(self):
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)

    def test_UserSettingsForm_valid_data(self):
        form = UserSettingsForm(data={
            'email':'test@gmail.com',
            'username':'test',
            'first_name':'test',
            'last_name':'test',
        })
        self.assertTrue(form.is_valid())

    def test_UserSettingsForm_no_data(self):
        form = UserSettingsForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    
    def test_PasswordChangeForm_valid_data(self):
        form = MyPasswordChangeForm(user=self.user, data={
            'old_password':'secret',
            'new_password1':'testpassword',
            'new_password2':'testpassword',
        })
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_PasswordChangeForm_no_data(self):
        form = MyPasswordChangeForm(user=self.user, data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)
