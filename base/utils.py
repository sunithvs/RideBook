import os

from django.utils import timezone


def get_file_path(instance, filename):
    # Get the current timestamp
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    # Get the file extension
    extension = os.path.splitext(filename)[1]
    # Generate a new filename with the timestamp
    new_filename = f"eventsradar-{timestamp}{extension}"
    return os.path.join("uploads", new_filename)
