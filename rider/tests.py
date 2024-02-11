from django.urls import reverse
from rest_framework.test import APITestCase

from auth_login.models import User
from config.settings import locations
from driver.models import Driver
from .models import Ride




class RideViewSetTestCase(APITestCase):
    fixtures = ['auth_login/fixtures/auth_login.json', 'driver/fixtures/driver.json', ]

    def setUp(self):
        self.user = User.objects.create_user(email='test@gmail.com',
                                             full_name='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        Ride.objects.create(rider=self.user, name='Ride 1', pickup_location='POINT(1.234 1.234)',
                            dropoff_location='POINT(2.234 2.234)')

    def test_list_rides(self):
        response = self.client.get(reverse('ride-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Ride 1')

    def test_create_ride(self):
        response = self.client.post(reverse('ride-list'), {
            'name': 'Ride 2',
            'pickup_location': locations['karinkallathani'],
            'dropoff_location': locations['mannarkkad']
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ride.objects.count(), 2)

    def test_cancel_ride(self):
        response = self.client.post(reverse('ride-list'), {
            'name': 'Ride 2',
            'pickup_location': locations['karinkallathani'],
            'dropoff_location': locations['mannarkkad']
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ride.objects.count(), 2)
        ride = Ride.objects.get(name='Ride 2')
        drivers = ride.drivers.all()
        response = self.client.post(reverse('ride-cancel', kwargs={'pk': ride.id}))
        self.assertEqual(response.status_code, 200)
        ride.refresh_from_db()
        self.assertEqual(ride.status, 'CANCELLED')
        for driver in drivers:
            self.assertEqual(driver.ride_requests.filter(id=ride.id).exists(), False)

    def test_pending_ride_auto_cancel(self):
        response = self.client.post(reverse('ride-list'), {
            'name': 'Ride 3',
            'pickup_location': locations['karinkallathani'],
            'dropoff_location': locations['mannarkkad']
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ride.objects.count(), 2)
        response = self.client.post(reverse('ride-list'), {
            'name': 'Ride 4',
            'pickup_location': locations['karinkallathani'],
            'dropoff_location': locations['mannarkkad']
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ride.objects.count(), 3)
        response = self.client.post(reverse('ride-list'), {
            'name': 'Ride 5',
            'pickup_location': locations['karinkallathani'],
            'dropoff_location': locations['mannarkkad']
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ride.objects.count(), 4)

        self.assertEqual(Ride.objects.filter(status='CANCELLED').count(), 3)
        self.assertEqual(Ride.objects.filter(status='PENDING').count(), 1)

    def test_ride_allocation(self):
        response = self.client.post(reverse('ride-list'), {
            'name': 'Ride 1',
            'pickup_location': locations['perinthalmanna'],
            'dropoff_location': locations['mannarkkad']
        }, format='json')

        target_drivers = [
            'driver2@gmail.com',
            'driver1@gmail.com',
        ]
        self.assertEqual(response.status_code, 201)
        for driver in target_drivers:
            self.assertEqual(Driver.objects.get(user__email=driver).ride_requests.filter(name='Ride 1').exists(),
                             True)
        for driver in Driver.objects.exclude(user__email__in=target_drivers):
            self.assertEqual(driver.ride_requests.filter(name='Ride 1').exists(), False)
