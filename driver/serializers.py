from django.contrib.gis.geos import Point
from rest_framework import serializers

from .models import Driver


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = (
            'id', 'user', 'model', 'registration_number', 'color', 'location', 'available', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

    def validate_location(self, value):
        if 'latitude' not in value or 'longitude' not in value:
            print(type(value))
            raise serializers.ValidationError("Latitude and longitude are required.")
        try:
            latitude = float(value['latitude'])
            longitude = float(value['longitude'])
        except ValueError:
            raise serializers.ValidationError("Invalid latitude or longitude format.")
        return Point(longitude, latitude)

    def create(self, validated_data):
        # Get the user making the request from the context
        user = self.context['request'].user
        if Driver.objects.filter(user=user).exists():
            raise serializers.ValidationError("Driver already exists for this user.")
        driver = Driver.objects.create(user=user, **validated_data)
        return driver

    def update(self, instance, validated_data):
        location_data = validated_data.get('location')

        if location_data and isinstance(location_data, dict):
            # If location_data is a dictionary, convert it to a Point object
            validated_data['location'] = self.validate_location(location_data)
        return super().update(instance, validated_data)



