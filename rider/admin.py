from django.contrib import admin

from .models import Ride


# Register your models here.

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'rider', 'driver', 'pickup_location', 'dropoff_location', 'status', 'created_at', 'updated_at')
    search_fields = (
        'name', 'rider__user__email',)
    list_filter = ('status', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'rider', 'driver', 'pickup_location', 'dropoff_location', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Rejected Drivers', {
            'fields': ('rejected_drivers',),
            'classes': ('collapse',)
        }),

    )
