"""
base.py
Base Settings for Django Project
"""

from pathlib import Path

import environ

env = environ.Env()

environ.Env.read_env('.env')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY", default="django-insecure-cag@!muz(kv)t31hxk6w3b)^vzt62_n1wo8&@89)ueefs6p4-7")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

# Admin URL for the project
ADMIN_URL = env.str("ADMIN_URL", default="admin/")

# Allowed hosts
ALLOWED_HOSTS = ['*']

# CSRF settings
CSRF_TRUSTED_ORIGINS = []

# CORS settings
CORS_ORIGIN_WHITELIST = []
CORS_ORIGIN_ALLOW_ALL = False

# Google API client ID and secret
GOOGLE_CLIENT_ID = env.str("GOOGLE_CLIENT_ID", default="")
GOOGLE_CLIENT_SECRET = env.str("GOOGLE_CLIENT_SECRET", default="")

# Email settings
EMAIL_HOST = env.str("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)

# Installed apps
INSTALLED_APPS = [
    'daphne',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Third-party apps
THIRD_PARTY_APPS = [
    "rest_framework",
    'drf_yasg',
    'ckeditor',
    'rest_framework_simplejwt',
    'django.contrib.gis',
]

# Custom apps
CUSTOM_APPS = [
    "auth_login",
    'rider',
    'driver',
    'notifications',
]

INSTALLED_APPS += CUSTOM_APPS + THIRD_PARTY_APPS
ASGI_APPLICATION = "config.asgi.application"
# Application name
APPLICATION_NAME = 'RIDER'

# Login URL
LOGIN_URL = "/auth/login/pass/"

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #jwt middleware

]

# Root URL configuration
ROOT_URLCONF = 'config.urls'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Define channel layer
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",  # Use an appropriate backend for production
    },
}


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = "auth_login.User"

# MAX Circle Radius for optimal driver search
MAX_RADIUS = 10  # in KM
locations = {
    'karinkallathani': {
        'latitude': 10.953835531166668,
        'longitude': 76.31819526049492
    },
    'amminikkad': {
        'latitude': 10.972923883788043,
        'longitude': 76.27217966094805
    },
    'perinthalmanna': {
        'latitude': 10.976871402847019,
        'longitude': 76.21234777594263
    },
    'mannarkkad': {
        'latitude': 11.001866146835766,
        'longitude': 76.45459713276014
    },
    'cherpulassery': {
        'latitude': 10.871870434770171,
        'longitude': 76.31346687683643

    }
}
