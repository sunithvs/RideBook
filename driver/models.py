from django.contrib.gis.db import models

from auth_login.models import User


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    model = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    location = models.PointField(geography=True, blank=True, null=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    ride_requests = models.ManyToManyField('rider.Ride', related_name='drivers', blank=True)

    def __str__(self):
        return f"{self.user.full_name}'s {self.model}"
