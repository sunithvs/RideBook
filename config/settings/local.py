"""
local.py
Local Development Settings
"""

from .base import *

DEBUG = True
# Admin URL
ADMIN_URL = "admin/"

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': env.str('POSTGRES_DB'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('DB_HOST'),
        'PORT': env.str('DB_PORT'),
    }
}

# Static and media files
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_BASE_URL = "media"
MEDIA_URL = '/media/'

STATIC_ROOT = BASE_DIR / "staticfiles"  # Replace with your staging static files directory
STATIC_URL = '/static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings - allow all origins
CORS_ORIGIN_ALLOW_ALL = True

# Additional allowed hosts
ALLOWED_HOSTS += ["*"]

# Additional trusted CSRF origins
CSRF_TRUSTED_ORIGINS += [
    "http://localhost:8000",
]

# Additional CORS origins whitelist
CORS_ORIGIN_WHITELIST += [
    "http://localhost:8000",
]
