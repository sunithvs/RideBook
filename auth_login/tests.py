from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


class AccountTests(APITestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_without_verification = User.objects.create_user(
            email="test@gmail.com", password="test1234", full_name="test")
        self.user_with_verification = User.objects.create_user(
            email="test1@gmail.com",
            password="test1234",
            full_name="test1",
            is_verified=True)
        self.profile_url = reverse('profile')

    def test_profile_without_verification(self):
        self.client.force_authenticate(user=self.user_without_verification)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_verified'], False)
        self.assertEqual(response.data['profile_completed'], False)

    def test_profile_with_verification(self):
        self.client.force_authenticate(user=self.user_with_verification)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_verified'], True)
        self.assertEqual(response.data['profile_completed'], False)
