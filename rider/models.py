import logging

from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from auth_login.models import User
from driver.models import Driver
from rider.utils import add_ride_to_driver_ride_requests

logger = logging.getLogger("rider")


class Ride(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    # name for testing purposes
    name = models.CharField(max_length=255, default='Ride')
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_rider')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='rides_as_driver', null=True, blank=True)
    pickup_location = models.PointField(geography=True, blank=True, null=True)
    dropoff_location = models.PointField(geography=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    eta = models.DateTimeField(blank=True, null=True)
    rejected_drivers = models.ManyToManyField(Driver, related_name='rejected_rides', blank=True)

    def distance(self):
        if self.pickup_location and self.dropoff_location:
            return self.pickup_location.distance(self.dropoff_location) * 100
        return 0

    def __str__(self):
        return f"Ride {self.id} - {self.rider.full_name} to {self.driver.user.full_name if self.driver else None} "

    class Meta:
        ordering = ['-created_at']

    def cancel(self):
        self.status = 'CANCELLED'
        self.drivers.clear()
        self.save()

    @property
    def can_cancel(self):
        return self.status == 'PENDING'


@receiver(post_save, sender=Ride)
def handle_ride_creation(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Ride {instance.id} created for {instance.rider.full_name}")
        add_ride_to_driver_ride_requests(instance)
