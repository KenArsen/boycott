from .base import *

# Development-specific settings
DEBUG = True

# Allow all hosts during development
ALLOWED_HOSTS = ["*"]

# Development database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Development-specific email backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Static files
STATIC_URL = "static/"
MEDIA_URL = "media/"
