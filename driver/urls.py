from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DriverViewSet, DriverRideViewSet

router = DefaultRouter()

router.register('ride', DriverRideViewSet, basename='driver-ride')
urlpatterns = [
    path('', DriverViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'patch': 'perform_update',
        'delete': 'perform_destroy'
    })),
    path('', include(router.urls)),

]
