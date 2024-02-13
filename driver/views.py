import logging

from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from base.permissions import IsDriver
from notifications.utils import send_message_to_channel
from rider.models import Ride
from rider.serializers import DriverRideSerializer
from rider.utils import add_ride_to_driver_ride_requests
from .models import Driver
from .serializers import DriverSerializer

logger = logging.getLogger("rider")


class DriverViewSet(viewsets.ViewSet):
    """
    A viewset for handling Driver operations.

    serializer_class -- The serializer class for Driver model.
    permission_classes -- Only authenticated users are allowed.
    """

    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Get the queryset filtered by the current user.

        Returns:
        Queryset -- Filtered Driver objects for the current user.
        """
        return Driver.objects.filter(user=self.request.user)

    def list(self, request):
        """
        List the details of the logged-in Driver.

        Returns:
        Response -- Serialized Driver details.
        """
        drivers = self.get_queryset().first()
        if drivers is None:
            logger.error("Driver not found for user: %s", request.user)
            return Response({"detail": "Driver not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(drivers, many=False)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new Driver instance.

        Returns:
        Response -- Serialized Driver details with HTTP 201 Created status.
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.info("Driver created for user: %s", request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, request):
        """
        Update the details of the logged-in Driver.

        Returns:
        Response -- Serialized updated Driver details.
        """
        driver = self.get_queryset().first()
        if driver is None:
            logger.error("Driver not found for user: %s", request.user)
            return Response({"detail": "Driver not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(driver, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.info("Driver updated for user: %s", request.user)
        return Response(serializer.data)

    def perform_destroy(self, request):
        """
        Delete the logged-in Driver.

        Returns:
        Response -- HTTP 204 No Content on successful deletion.
        """
        driver = self.get_queryset().first()
        if driver is None:
            logger.error("Driver not found for user: %s", request.user)
            return Response({"detail": "Driver not found."}, status=status.HTTP_404_NOT_FOUND)

        driver.delete()

        logger.info("Driver deleted for user: %s", request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DriverRideViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling DriverRide operations.

    queryset -- All Ride objects.
    serializer_class -- The serializer class for DriverRide model.
    permission_classes -- Only drivers are allowed.
    pagination_class -- PageNumberPagination for listing rides.
    http_method_names -- Only allow GET and POST methods.
    """

    queryset = Ride.objects.all()
    serializer_class = DriverRideSerializer
    permission_classes = [IsDriver]
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post']

    def get_queryset(self):
        """
        Get the queryset filtered based on the user's role.

        Returns:
        Queryset -- Filtered Ride objects for the current user.
        """
        if self.request.user.is_anonymous:
            return Ride.objects.none()
        driver_rides = Ride.objects.filter(driver=self.request.user.driver)
        ride_requests = self.request.user.driver.ride_requests.all()
        return driver_rides | ride_requests

    def perform_create(self, serializer):
        """
        This method is intentionally left empty as the creation of a new DriverRide instance
        is not supported in this viewset.

        Args:
        serializer -- The serializer instance.
        Raises:
        MethodNotAllowed -- Always raised to indicate that creating a new DriverRide instance
                            is not allowed in this viewset.

        Returns:
        None
        """
        # The creation of a new DriverRide instance is not allowed in this viewset.
        # Raise MethodNotAllowed to indicate that this operation is not supported.

        logger.warning("perform_create method called, but creating a new DriverRide instance is not allowed.")
        raise MethodNotAllowed("Creating a new DriverRide instance is not supported ")

    @swagger_auto_schema(
        methods=['post'],
        operation_summary='Accept a ride',
        operation_description='Accept a ride',
        responses={200: 'Ride accepted', 400: 'Ride cannot be accepted'},
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT),  # Empty request body
    )
    @action(detail=True, methods=['post'], url_path='accept', url_name='accept_ride')
    def accept_ride(self, request, pk=None):
        """
        Accept a ride request and update the ride status.

        Returns:
        Response -- HTTP 200 on success, HTTP 400 on failure.
        """
        ride = self.get_object()
        driver = request.user.driver

        if ride.driver or not driver.available:
            logger.warning("Ride cannot be accepted. Driver not available or already assigned.")
            return Response({'message': 'Ride cannot be accepted'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            driver.available = False
            driver.save()
            ride.drivers.clear()
            driver.ride_requests.clear()
            send_message_to_channel(f"notification__{driver.user.id}", "Ride Accept")
            ride.driver = driver
            ride.status = 'IN_PROGRESS'
            ride.save()

        logger.info("Ride accepted by driver %s for ride %s", driver.user.full_name, ride.id)
        return Response({'message': 'Ride accepted'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=['post'],
        operation_summary='Complete a ride',
        operation_description='Complete a ride',
        responses={200: 'Ride completed', 400: 'Ride cannot be completed'},
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT),  # Empty request body
    )
    @action(detail=True, methods=['post'], url_path='complete', url_name='complete_ride')
    def complete_ride(self, request, pk=None):
        """
        Mark a ride as completed.

        Returns:
        Response -- HTTP 200 on success, HTTP 400 on failure.
        """
        ride = self.get_object()
        driver = request.user.driver
        ride = driver.rides_as_driver.get(id=ride.id)
        if ride and ride.status != 'IN_PROGRESS' and ride.pk != pk:
            logger.warning("Invalid Request to complete ride.")
            return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            driver.available = True
            driver.save()
            ride.status = 'COMPLETED'
            ride.save()

        logger.info("Ride completed by driver %s for ride %s", driver.user.full_name, ride.id)
        return Response({'message': 'Ride completed'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=['post'],
        operation_summary='Cancel a ride',
        operation_description='Cancel a ride',
        responses={200: 'Ride cancelled', 400: 'Ride cannot be cancelled'},
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT),  # Empty request body
    )
    @action(detail=True, methods=['post'], url_path='reject', url_name='reject_ride')
    def reject_ride(self, request, pk=None):
        """
        Reject a ride request and find an optimal driver for the ride.

        Returns:
        Response -- HTTP 200 on success, HTTP 400 on failure.
        """
        logger.info(f"Rejecting ride {self.get_object().id}")
        ride = self.get_object()
        driver = request.user.driver
        with transaction.atomic():
            logger.info(f"Rejecting ride {ride.id} for {driver.user.full_name}")
            ride.rejected_drivers.add(driver)
            ride.save()
            driver.ride_requests.remove(ride)
            driver.save()
            logger.info(f"Finding optimal driver for ride {ride.id}")
            add_ride_to_driver_ride_requests(ride)

        logger.info("Ride rejected by driver %s for ride %s", driver.user.full_name, ride.id)
        return Response({'message': 'Ride cancelled'}, status=status.HTTP_200_OK)
