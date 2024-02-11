from django.urls import reverse
from rest_framework.test import APITestCase

from auth_login.models import User
from .models import Ride


class RideViewSetTestCase(APITestCase):
    fixtures = ['auth_login/fixtures/auth_login.json', 'driver/fixtures/driver.json', ]

    def setUp(self):
        self.user = User.objects.create_user(email='test@gmail.com', full_name='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        Ride.objects.create(rider=self.user, name='Ride 1', pickup_location='POINT(1.234 1.234)',
                            dropoff_location='POINT(2.234 2.234)')
        self.locations = {
            'karinkallathani': {
                'latitude': 10.953835531166668,
                'longitude': 76.31819526049492
            },
            'amminikkad': {
                'latitude': 10.972923883788043,
                'longitude': 76.27217966094805
            },
            'perinthalmanna': {
                'latitude': 10.976871402847019,
                'longitude': 76.21234777594263
            },
            'mannarkkad': {
                'latitude': 11.001866146835766,
                'longitude': 76.45459713276014
            },
            'cherpulassery': {
                'latitude': 10.871870434770171,
                'longitude': 76.31346687683643

            }
        }

    def test_list_rides(self):
        response = self.client.get(reverse('ride-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Ride 1')

    def test_create_ride(self):
        response = self.client.post(reverse('ride-list'), {
            'name': 'Ride 2',
            'pickup_location': self.locations['karinkallathani'],
            'dropoff_location': self.locations['mannarkkad']
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ride.objects.count(), 2)

    def test_cancel_ride(self):
        response = self.client.post(reverse('ride-cancel', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ride.objects.get(pk=1).status, 'CANCELLED')
        response = self.client.post(reverse('ride-cancel', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Ride.objects.get(pk=1).status, 'CANCELLED')

    def test_pending_ride_auto_cancel(self):
        response = self.client.post(reverse('ride-list'), {
            'name': 'Ride 3',
            'pickup_location': self.locations['karinkallathani'],
            'dropoff_location': self.locations['mannarkkad']
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ride.objects.count(), 2)
        response = self.client.post(reverse('ride-list'), {
            'name': 'Ride 4',
            'pickup_location': self.locations['karinkallathani'],
            'dropoff_location': self.locations['mannarkkad']
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ride.objects.count(), 3)
        response = self.client.post(reverse('ride-list'), {
            'name': 'Ride 5',
            'pickup_location': self.locations['karinkallathani'],
            'dropoff_location': self.locations['mannarkkad']
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ride.objects.count(), 4)

        self.assertEqual(Ride.objects.filter(status='CANCELLED').count(), 3)
        self.assertEqual(Ride.objects.filter(status='PENDING').count(), 1)


