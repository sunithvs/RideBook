# utils.py
import logging

from django.contrib.gis.db.models.functions import Distance
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from driver.models import Driver

logger = logging.getLogger("rider")


def add_ride_to_driver_ride_requests(ride):
    if ride.pickup_location:
        logger.info(f"Finding optimal driver for ride {ride.id}")
        optimal_driver = find_optimal_driver(ride)
        logger.info(f"Optimal driver for ride {ride.id} is {optimal_driver}")

        if optimal_driver:
            optimal_driver.ride_requests.add(ride)
            logger.info(f"Ride {ride.id} added to driver {optimal_driver.id} ride requests")


def find_optimal_driver(ride):
    pickup_location = ride.pickup_location
    logger.info(f"Finding optimal driver for pickup location {pickup_location}")
    try:
        optimal_driver = Driver.objects.filter(
            available=True,
            location__isnull=False,  # Ensure the driver has a valid location
        ).exclude(
            id__in=ride.rejected_drivers.all()  # Exclude drivers who have rejected this ride
        ).annotate(
            distance=Distance('location', pickup_location),
        ).filter(
            Q(ride_requests__isnull=True) | Q(ride_requests__status__in=['COMPLETED', 'CANCELLED'])
        ).order_by('distance').first()

        logger.info(f"Optimal driver found for pickup location {pickup_location}: {optimal_driver}")

        return optimal_driver if optimal_driver else None
    except ObjectDoesNotExist:
        logger.error(f"No optimal driver found for pickup location {pickup_location}")
        return None
    except Exception as e:
        logger.error(f"Error finding optimal driver for pickup location {pickup_location}: {e}")
        return None
