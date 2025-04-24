from .base import *

# Override the storage configuration for local development
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": os.path.join(BASE_DIR, "media"),
            "base_url": "/media/",
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Create media directory if it doesn't exist
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
os.makedirs(MEDIA_ROOT, exist_ok=True)

# Set debug to True for development
DEBUG = True

# Add media serving for development
MIDDLEWARE += [
    'django.contrib.staticfiles.middleware.StaticFilesMiddleware',
]

# Allow all hosts in development
ALLOWED_HOSTS = ["*"]