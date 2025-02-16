from .base import *

# Development-specific settings
DEBUG = True

DOMAIN = "http://localhost:8000"

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
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
