from django.contrib.gis.forms import PointField
from django.contrib.gis.geos import Point
from rest_framework import serializers

from rider.models import Ride


class RideSerializer(serializers.ModelSerializer):
    pickup_location = PointField()
    dropoff_location = PointField()

    class Meta:
        model = Ride
        fields = ['id', 'name', 'rider', 'driver', 'pickup_location', 'dropoff_location',
                  'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'status', 'rider', 'driver']

    def validate_location_data(self, location_data):
        if 'latitude' not in location_data or 'longitude' not in location_data:
            raise serializers.ValidationError("Latitude and longitude are required.")

        try:
            latitude = float(location_data['latitude'])
            longitude = float(location_data['longitude'])
        except ValueError:
            raise serializers.ValidationError("Invalid latitude or longitude format.")
        return Point(longitude, latitude)

    def create(self, validated_data):
        dropoff_location_data = validated_data.pop('dropoff_location', {})
        pickup_location_data = validated_data.pop('pickup_location', {})

        dropoff_location = self.validate_location_data(dropoff_location_data)
        pickup_location = self.validate_location_data(pickup_location_data)

        ride = Ride.objects.create(pickup_location=pickup_location, dropoff_location=dropoff_location, **validated_data)
        return ride


class DriverRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'rider', 'pickup_location', 'dropoff_location', 'status']
        read_only_fields = ['id', 'rider', 'pickup_location', 'dropoff_location', 'status']
