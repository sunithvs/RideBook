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
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return Ride.objects.filter(rider=self.request.user)

    def perform_create(self, serializer):
        # cancel any pending rides
        rides = Ride.objects.filter(rider=self.request.user, status='PENDING')
        logger.info(f"Rides to cancel: {rides}")
        for ride in rides:
            ride.cancel()
        serializer.save(rider=self.request.user)

    # extra action to cancel a ride
    @swagger_auto_schema(
        methods=['post'],
        operation_summary='Cancel a ride',
        operation_description='Cancel a ride',
        responses={200: 'Ride cancelled', 400: 'Ride cannot be cancelled'},
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT),  # Empty request body

    )
    @action(detail=True, methods=['post'], url_path='cancel', url_name='cancel')
    def cancel(self, request, pk=None):
        if not self.get_object().can_cancel:
            return Response({'message': 'ride cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)
        self.get_object().cancel()
        return Response({'message': 'ride cancelled'}, status=status.HTTP_200_OK)
