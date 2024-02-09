from django.contrib.gis.db import models

from auth_login.models import User


class Ride(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_rider')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_driver', null=True, blank=True)
    pickup_location = models.PointField(geography=True, blank=True, null=True)
    dropoff_location = models.PointField(geography=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    eta = models.DateTimeField(blank=True, null=True)

    def distance(self):
        if self.pickup_location and self.dropoff_location:
            return self.pickup_location.distance(self.dropoff_location) * 100
        return 0

    def __str__(self):
        return f"Ride {self.id} - {self.rider.full_name} to {self.driver.full_name}"

    class Meta:
        ordering = ['-created_at']

    def cancel(self):
        self.status = 'CANCELLED'
        self.save()

    @property
    def can_cancel(self):
        return self.status == 'PENDING'
