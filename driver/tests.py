from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_login.models import User
from driver.models import Driver


# Create your tests here.
class DriverViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='@x3cvx#sf124t',
            full_name='Test User',
            mobile_number='1234567890'
        )
        self.client.force_authenticate(user=self.user)
        self.driver_data = {
            'model': 'Test Model',
            'registration_number': 'ABC123',
            'color': 'Red',
            'location': {
                'latitude': '1.234',
                'longitude': '1.234'
            },
            'available': True,
        }

    def test_create_driver(self):
        response = self.client.post(reverse('driver'), self.driver_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)
        self.assertEqual(Driver.objects.get().user, self.user)

    def test_list_drivers(self):
        Driver.objects.create(
            user=self.user,
            model='Test Model',
            registration_number='ABC123',
            color='Red',
            location='POINT(1.234 1.234)',
            available=True
        )
        response = self.client.get(reverse('driver'))
        if response.status_code == status.HTTP_200_OK:
            self.assertGreater(len(response.data), 0)
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            self.assertEqual(len(response.data), 0)
        else:
            self.fail(f"Unexpected response status: {response.status_code}")

    def test_update_driver(self):
        driver = Driver.objects.create(
            user=self.user,
            model='Test Model',
            registration_number='ABC123',
            color='Red',
            location='POINT(1.234 1.234)',
            available=True
        )
        update_data = {
            'model': 'New Test Model',
            'registration_number': 'XYZ123',
            'color': 'Blue',
            'location': {
                'latitude': '3.234',
                'longitude': '2.234'
            },
            'available': False,
        }
        response = self.client.patch(reverse('driver'), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        driver.refresh_from_db()
        self.assertEqual(driver.model, 'New Test Model')
        self.assertEqual(driver.registration_number, 'XYZ123')
        self.assertEqual(driver.color, 'Blue')
        self.assertEqual(driver.location.x, 2.234)
        self.assertEqual(driver.location.y, 3.234)
        self.assertEqual(driver.available, False)

    def test_delete_driver(self):
        driver = Driver.objects.create(
            user=self.user,
            model='Test Model',
            registration_number='ABC123',
            color='Red',
            location='POINT(1.234 1.234)',
            available=True
        )
        response = self.client.delete(reverse('driver'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Driver.objects.count(), 0)
        self.assertEqual(User.objects.count(), 1)
