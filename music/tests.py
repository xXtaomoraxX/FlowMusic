from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.

class RegisterViewTest(TestCase):
    def test_register_view(self):
        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_create_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'juan1234',
            'email': 'juan1234@example.com',
            'password': 'password123',
        })

        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='juan1234').exists())

    def test_create_user_password_too_short(self):
        response = self.client.post(reverse('register'), {
            'username': 'juan1234',
            'email': 'juan1234@example.com',
            'password': 'pass',
        })

        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username='juan1234').exists())

    def test_duplicate_username(self):
        self.test_create_user()

        response = self.client.post(reverse('register'), {
            'username': 'juan1234',
            'email': 'juan1234@example.com',
            'password': 'password123',
        })

        self.assertContains(response, 'Username already exists', status_code=400)

    def test_duplicate_email(self):
        self.test_create_user()

        response = self.client.post(reverse('register'), {
            'username': 'juan12343',
            'email': 'juan1234@example.com',
            'password': 'password123',
        })

        self.assertContains(response, 'Email already exists', status_code=400)

    def test_empty_fields(self):
        response = self.client.post(reverse('register'), {
            'username': '',
            'email': '',
            'password': '',
        })

        self.assertContains(response, 'All fields are required', status_code=400)
