from django.urls import path

from .views import DriverViewSet

urlpatterns = [
    path('', DriverViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'patch': 'perform_update',
        'delete': 'perform_destroy'
    }))]
