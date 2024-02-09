from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rider.views import RideViewSet

router = DefaultRouter()
router.register('', RideViewSet, basename='ride')

urlpatterns = [
    path('', include(router.urls)),
]
