# utils.py
import logging

from django.contrib.gis.db.models.functions import Distance
from django.core.exceptions import ObjectDoesNotExist

from config.settings import MAX_RADIUS
from driver.models import Driver
from notifications.utils import send_message_to_channel

logger = logging.getLogger("rider")


def add_ride_to_driver_ride_requests(ride):
    """
    Add a ride to the ride requests of optimal drivers.

    If the ride has a pickup location, find optimal drivers for that location
    and add the ride to their ride requests.

    Args:
    ride -- The Ride instance.

    Returns:
    None
    """
    if ride.pickup_location:
        logger.info(f"Finding optimal driver for ride {ride.id}")
        optimal_driver = find_optimal_drivers(ride)
        logger.info(f"Optimal drivers for ride {ride.id}: {optimal_driver.count() if optimal_driver else 0}")

        for driver in optimal_driver:
            driver.ride_requests.add(ride)
            logger.info(f"Ride {ride.id} added to driver {driver.id} ride requests")
            try:
                send_message_to_channel(f"notification__{driver.user.id}", "Ride request")
                logger.info(f"Notification sent to driver {driver.id} for ride {ride.id}")
            except Exception as e:
                logger.error(f"Error sending notification to driver {driver.id} for ride {ride.id}: {e}")


def find_optimal_drivers(ride):
    """
    Find optimal drivers for a ride based on the pickup location.

    Optimal drivers are those who are available, have a location, and are within
    a certain distance from the ride's pickup location.

    Args:
    ride -- The Ride instance.

    Returns:
    Queryset -- Queryset of optimal Driver instances.
    """
    pickup_location = ride.pickup_location
    logger.info(f"Finding optimal driver for pickup location {pickup_location}")
    try:
        optimal_driver = Driver.objects.filter(
            available=True,
            location__isnull=False,
        ).exclude(
            id__in=ride.rejected_drivers.all()
        ).annotate(
            distance=Distance('location', pickup_location),
        ).filter(
            distance__lte=MAX_RADIUS*1000,  # Filter drivers within 10 km
        )
        logger.info(f"Optimal drivers found for pickup location {pickup_location}: {optimal_driver}")

        return optimal_driver
    except ObjectDoesNotExist:
        logger.error(f"No optimal driver found for pickup location {pickup_location}")
        return Driver.objects.none()
    except Exception as e:
        logger.error(f"Error finding optimal driver for pickup location {pickup_location}: {e}")
        return Driver.objects.none()
