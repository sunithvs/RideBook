from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_login.models import User


class SignUpViewTest(APITestCase):
    def setUp(self):
        self.signup_url = reverse('signup')

    def test_valid_signup(self):
        data = {
            'email': 'test@example.com',
            'password': 'D@dsf12casd',
            'mobile_number': '1234567890',
            'full_name': 'test'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_duplicate_email(self):
        User.objects.create_user(full_name='test', email='test@example.com', password='D@dsf12casd')

        data = {
            'email': 'test@example.com',
            'password': 'D@dsf12casd',
            'mobile_number': '1234567890',
            'full_name': 'test'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email(self):
        data = {
            'email': 'test',
            'password': 'D@dsf12casd',
            'mobile_number': '1234567890',
            'full_name': 'test'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_mobile(self):
        data = {
            'email': 'test',
            'password': 'D@dsf12casd',
            'mobile_number': '123',
            'full_name': 'test'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginViewTest(APITestCase):
    def setUp(self):
        self.login_url = reverse('login')  # Replace 'login' with the actual name of your login URL
        self.user_data = {
            'email': 'test@example.com',
            'password': 'D@dsf12casd',
        }
        self.user = User.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            full_name='Sunith VS',
            mobile_number='+919072124291',
        )

    def test_valid_login(self):
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_invalid_password(self):
        self.user_data['password'] = 'wrongpassword'
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Invalid email or password')

    def test_user_not_found(self):
        self.user_data['email'] = 'nonexistent@example.com'  # Nonexistent email
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Invalid email or password')

    def test_missing_email_or_password(self):
        invalid_data = {}
        response = self.client.post(self.login_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'email and password are required')

