from django.test import TestCase, Client
from django.urls import reverse
from .models import *

class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.login  = reverse("login")
        self.credentials = {
            'username': 'arash1',
            'password': 'arash1'}
        user = User.objects.create_user(**self.credentials)

    def test_loginview_GET(self):    
        response = self.client.get(self.login)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_loginview_POST(self):
        response = self.client.post(self.login, data=self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

