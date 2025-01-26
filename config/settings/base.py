from pathlib import Path

from django.conf.locale import LANG_INFO
from django.utils.translation import gettext_lazy as _

from .environment import env

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env.str("SECRET_KEY")

INSTALLED_APPS = [
    # first party apps
    "jazzmin",
    "modeltranslation",
    # second party apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # third party apps
    #
    # local apps
    "apps.common.apps.CommonConfig",
    "apps.user.apps.UserConfig",
    "apps.product.apps.ProductConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
AUTH_USER_MODEL = "user.User"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

JAZZMIN_SETTINGS = {
    "site_title": "Boycott Admin",
    "site_header": "Boycott",
    "site_brand": "Boycott",
    "site_logo_classes": "img-circle",
    "welcome_sign": "Welcome to the Boycott Admin!",
    "search_model": ["user.User", "product.Product"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Users", "model": "user.User", "url": "/admin/user/user/"},
        {
            "name": "Products",
            "model": "product.Product",
            "url": "/admin/product/product/",
        },
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["user"],
    "icons": {
        # Users
        "user": "fas fa-users-cog",
        "user.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "user.Invitation": "fas fa-envelope-open-text",
        # Sites
        "sites.Site": "fas fa-globe",
        # Products
        "product.Product": "fas fa-box",
        "product.Category": "fas fa-tags",
        "product.Reason": "fas fa-exclamation-triangle",
        "product.Review": "fas fa-comment-alt",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    "language_chooser": True,
}

EMAIL_HOST = env.str("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)

# Internationalization settings
LANGUAGE_CODE = "ru-ru"
LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
    ("kg", _("Kyrgyz")),
]

MODELTRANSLATION_LANGUAGES = ("en", "ru", "kg")
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"

LANG_INFO.update(
    {
        "kg": {
            "bidi": False,
            "code": "kg",
            "name": "Kyrgyz",
            "name_local": "Кыргызча",
        },
    }
)

TIME_ZONE = env.str("TIME_ZONE", default="UTC")

USE_I18N = True
USE_L10N = True
USE_TZ = True

SITE_ID = env.int("SITE_ID", default=1)

LOCALE_PATHS = [BASE_DIR / "locale/"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
