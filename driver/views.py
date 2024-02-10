from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Driver
from .serializers import DriverSerializer


class DriverViewSet(viewsets.ViewSet):
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Driver.objects.filter(user=self.request.user)

    def list(self, request):
        drivers = self.get_queryset().first()
        if drivers is None:
            return Response({"detail": "Driver not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(drivers, many=False)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, request):
        # get pk from request.user.driver.id
        driver = self.get_queryset().first()
        print(driver, request.user.driver.id)
        if driver is None:
            return Response({"detail": "Driver not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(driver, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def perform_destroy(self, request):
        driver = self.get_queryset().first()
        if driver is None:
            return Response({"detail": "Driver not found."}, status=status.HTTP_404_NOT_FOUND)
        driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
