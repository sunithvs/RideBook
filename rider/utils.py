# utils.py
import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.gis.db.models.functions import Distance
from django.core.exceptions import ObjectDoesNotExist

from config.settings import MAX_RADIUS
from driver.models import Driver
from notifications.utils import send_message_to_channel

logger = logging.getLogger("rider")




def add_ride_to_driver_ride_requests(ride):
    if ride.pickup_location:
        logger.info(f"Finding optimal driver for ride {ride.id}")
        optimal_driver = find_optimal_drivers(ride)
        logger.info(f"Optimal drivers for ride {ride.id} is {optimal_driver.count() if optimal_driver else 0}")

        for driver in optimal_driver:
            driver.ride_requests.add(ride)
            logger.info(f"Ride {ride.id} added to driver {driver.id} ride requests")
            try:
                send_message_to_channel(f"notification__{driver.user.id}", "Ride request")
                print("send notification to ", driver)
            except Exception as e:
                print(e)





def find_optimal_drivers(ride):
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
        return None
    except Exception as e:
        logger.error(f"Error finding optimal driver for pickup location {pickup_location}: {e}")
        return None
