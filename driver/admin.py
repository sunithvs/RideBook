from django.contrib import admin

from .models import Driver


# Register your models here.

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'model', 'registration_number', 'color', 'location', 'available', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'model', 'registration_number', 'color')
    list_filter = ('available', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'model', 'registration_number', 'color', 'location', 'available')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        (
            'Ride Requests',
            {
                'fields': ('ride_requests',),
                'classes': ('collapse',)
            }
        )
    )
