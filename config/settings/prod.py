"""
prod.py
Staging Settings for Django Project
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allowed hosts
ALLOWED_HOSTS = [
    'ride.sunithvs.com',
]

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    'https://ride.sunithvs.com',
]

# CORS settings
CORS_ORIGIN_WHITELIST = [
    'https://ride.sunithvs.com',
]
CORS_ORIGIN_ALLOW_ALL = False

# Static and media files
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_BASE_URL = "media"
MEDIA_URL = '/media/'

STATIC_ROOT = BASE_DIR / "staticfiles"  # Replace with your staging static files directory
STATIC_URL = '/static/'

# Cache settings
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "radar_cache"
    }
}
