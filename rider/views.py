# Create your views here.
import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from rider.models import Ride
from rider.serializers import RideSerializer

logger = logging.getLogger("auth")


class RideViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling Ride operations.

    queryset -- All Ride objects.
    serializer_class -- The serializer class for Ride model.
    permission_classes -- Only authenticated users are allowed.
    pagination_class -- PageNumberPagination for listing rides.
    http_method_names -- Only allow GET and POST methods.
    """

    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post']

    def get_queryset(self):
        """
        Get the queryset filtered by the current user as the rider.

        Returns:
        Queryset -- Filtered Ride objects for the current user.
        """
        return Ride.objects.filter(rider=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new Ride instance.

        Cancels any pending rides for the current user before creating a new ride.

        Args:
        serializer -- The serializer instance.

        Returns:
        None
        """
        # Cancel any pending rides for the current user
        rides = Ride.objects.filter(rider=self.request.user, status='PENDING')
        logger.info(f"Cancelling pending rides for rider {self.request.user}: {rides}")
        for ride in rides:
            ride.cancel()

        # Save the new ride instance with the current user as the rider
        serializer.save(rider=self.request.user)

        logger.info(f"New ride created for rider {self.request.user}")

    @swagger_auto_schema(
        methods=['post'],
        operation_summary='Cancel a ride',
        operation_description='Cancel a ride',
        responses={200: 'Ride cancelled', 400: 'Ride cannot be cancelled'},
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT),  # Empty request body
    )
    @action(detail=True, methods=['post'], url_path='cancel', url_name='cancel')
    def cancel(self, request, pk=None):
        """
        Cancel a ride.

        Returns:
        Response -- HTTP 200 on success, HTTP 400 on failure.
        """
        ride = self.get_object()

        if not ride.can_cancel:
            logger.warning(f"Ride {ride.id} cannot be cancelled.")
            return Response({'message': 'Ride cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)

        ride.cancel()

        logger.info(f"Ride {ride.id} cancelled by rider {request.user}")
        return Response({'message': 'Ride cancelled'}, status=status.HTTP_200_OK)
