from pathlib import Path

from .environment import env

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env.str("SECRET_KEY")

INSTALLED_APPS = [
    # first party apps
    "jazzmin",
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

# AUTH_USER_MODEL = "account.User"
ROOT_URLCONF = "config.urls"

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
    "search_model": ["account.User"],
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Users", "model": "account.User", "url": "/admin/account/user/"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["user"],
    "icons": {
        # Users
        "user": "fas fa-users-cog",
        "account.User": "fas fa-user",
        "account.Profile": "fas fa-id-card",
        "account.Invitation": "fas fa-envelope-open-text",
        "user.Group": "fas fa-users",
        # Sites
        "sites.Site": "fas fa-globe",
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
    # "language_chooser": True,
}

LANGUAGE_CODE = "ru-ru"

# LANGUAGES = [
#     ("en", _("English")),
#     ("ru", _("Russian")),
# ]
#
# MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
# MODELTRANSLATION_LANGUAGES = ("en", "ru")
#
# LOCALE_PATHS = [BASE_DIR / "locale/"]

TIME_ZONE = env.str("TIME_ZONE", default="UTC")

USE_I18N = True

USE_TZ = True

SITE_ID = env.int("SITE_ID", default=1)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
