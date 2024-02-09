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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('POSTGRES_DB'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('DB_HOST'),
        'PORT': env.str('DB_PORT'),
    }
}

# Static files URL
STATIC_URL = '/static/'

# Media files URL
MEDIA_URL = '/media/'

# Base URL for media files (e.g., when serving from a different domain)
MEDIA_BASE_URL = "http://localhost:3000"

# Additional directories to search for static files
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Custom user model


# Media root directory
MEDIA_ROOT = BASE_DIR / 'media'

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
