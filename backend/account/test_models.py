from django.utils.text import slugify
from django.test import TestCase
from .models import*

class TestModels(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(
            username = 'testusername',
            email = 'test@gmail.com',
            first_name = 'testfirstname',
            last_name = 'testlastname',
        )
        self.user.set_password('secret')
        self.user.save()
    
    def test_UserModel(self):
        self.assertEquals("test@gmail.com", self.user.email)
        self.assertEquals("testusername", self.user.username)
        self.assertEquals("testfirstname", self.user.first_name)
        self.assertEquals("testlastname", self.user.last_name)
        self.assertTrue(self.user.check_password('secret'))   

    def test_create_user(self):
        user = User.objects.create_user(
            username="test2", email='test2@gmail.com', password='test2')
        self.assertEqual(user.email, 'test2@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username="test2", email='test2@gmail.com', password='test2')
        self.assertEqual(admin_user.email, 'test2@gmail.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)