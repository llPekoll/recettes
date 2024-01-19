"""
Django settings for elisasrecipe project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _

DEBUG = "DEBUG" in os.environ
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get("SECRET_KEY", "José Martins")

INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS = [
    "versatileimagefield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "recipe",
    "account",
    "django_htmx",
    "storages",
    "django_quill",
    "common",
    "article",
    "easyaudit",
    "tailwind",
    "theme",
    "django_browser_reload",
]


TAILWIND_APP_NAME = "theme"

MIDDLEWARE = [
    # "elisasrecipe.middleware.RemoveDataTestMiddleware",
    "easyaudit.middleware.easyaudit.EasyAuditMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "elisasrecipe.urls"

if DEBUG:
    X_FRAME_OPTIONS = "SAMEORIGIN"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "base/templates"),
            os.path.join(BASE_DIR, "accounts/templates"),
            os.path.join(BASE_DIR, "elisasrecipe/templates"),
            os.path.join(BASE_DIR, "common/templates"),
            os.path.join(BASE_DIR, "articles/templates"),
        ],
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
if DEBUG:
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                os.path.join(BASE_DIR, "base/templates"),
                os.path.join(BASE_DIR, "accounts/templates"),
                os.path.join(BASE_DIR, "elisasrecipe/templates"),
                os.path.join(BASE_DIR, "common/templates"),
                os.path.join(BASE_DIR, "articles/templates"),
            ],
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

WSGI_APPLICATION = "elisasrecipe.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("PGUSER", "user"),
        "PASSWORD": os.environ.get("PGPASSWORD", "password"),
        "HOST": os.environ.get("PGHOST", "localhost"),
        "PORT": os.environ.get("PGPORT", "5432"),
    }
}


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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale/"),)
LANGUAGE_CODE = "en"
LANGUAGES = (
    ("en", _("English")),
    ("fr", _("Francais")),
    ("es", _("Espagnol")),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGOUT_REDIRECT_URL = "home"


AUTH_USER_MODEL = "account.User"


TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


APIKEY_MAILWIND = os.environ.get("APIKEY_MAILWIND")


AWS_ACCESS_KEY_ID = os.getenv("MINIO_ROOT_USER") or os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("MINIO_ROOT_PASSWORD") or os.getenv(
    "AWS_SECRET_ACCESS_KEY"
)
AWS_STORAGE_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME") or os.getenv(
    "AWS_STORAGE_BUCKET_NAME"
)
AWS_S3_ENDPOINT_URL = os.getenv("MINIO_ENDPOINT") or os.getenv("AWS_S3_ENDPOINT_URL")
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_DEFAULT_ACL = "private-read"
AWS_LOCATION = "static"
# STATICFILES_STORAGE = 'elisasrecipe.storage_backends.StaticStorage'

STATIC_URL = f"{AWS_S3_ENDPOINT_URL}static/"
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        # Leave whatever setting you already have here, e.g.:
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
}
if "MINIO_ROOT_USER" in os.environ:
    MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
    MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")
    MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
    AWS_ACCESS_KEY_ID = MINIO_ACCESS_KEY
    AWS_SECRET_ACCESS_KEY = MINIO_SECRET_KEY
    AWS_STORAGE_BUCKET_NAME = MINIO_BUCKET_NAME
    AWS_S3_ENDPOINT_URL = MINIO_ENDPOINT
    STATIC_URL = "static/"
    MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = True
    # AWS_S3_FILE_OVERWRITE = False

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            # Leave whatever setting you already have here, e.g.:
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

STATIC_ROOT = "staticfiles/"

STATICFILES_DIRS = [BASE_DIR / "static"]


# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
# MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")
# MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
# MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
# AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
# AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")
# AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
# AWS_ACCESS_KEY_ID = MINIO_ACCESS_KEY
# AWS_SECRET_ACCESS_KEY = MINIO_SECRET_KEY
# AWS_STORAGE_BUCKET_NAME = MINIO_BUCKET_NAME
# AWS_S3_ENDPOINT_URL = MINIO_ENDPOINT

# AWS_S3_FILE_OVERWRITE = False


QUILL_CONFIGS = {
    "default": {
        "theme": "bubble",
        "modules": {
            "syntax": True,
            "toolbar": [
                [
                    {"font": []},
                    {"size": []},
                    # {"header": []},
                    # {"align": []},
                    "bold",
                    "italic",
                    "underline",
                    "strike",
                    # "blockquote",
                    # {"color": []},
                    # {"background": []},
                ],
                [
                    {"list": "ordered"},
                    {"list": "bullet"},
                    # "code-block",
                    # "link",
                    # "image",
                ],
            ],
        },
    },
    "article": {
        "theme": "bubble",
        "modules": {
            "syntax": True,
            "toolbar": [
                [
                    {"header": []},
                    "bold",
                    "italic",
                    "underline",
                    "strike",
                    "blockquote",
                ],
                [
                    {"list": "ordered"},
                    {"list": "bullet"},
                    "link",
                    "image",
                ],
            ],
        },
    },
    "comment": {
        "theme": "bubble",
        "modules": {
            "syntax": True,
            "toolbar": [
                [
                    "bold",
                    "italic",
                    "strike",
                ],
            ],
        },
    },
    "recipe": {
        "theme": "bubble",
        "modules": {
            "syntax": True,
            "toolbar": [
                [
                    "strike",
                    "bold",
                    "italic",
                ],
            ],
        },
    },
}


# Minimum similarity threshold for trigram similarity search
PG_TRGM_DEFAULT_SIMILARITY_THRESHOLD = 0.1


VERSATILEIMAGEFIELD_SETTINGS = {
    # The amount of time, in seconds, that references to created images
    # should be stored in the cache. Defaults to `2592000` (30 days)
    "cache_length": 2592000,
    # The name of the cache you'd like `django-versatileimagefield` to use.
    # Defaults to 'versatileimagefield_cache'. If no cache exists with the name
    # provided, the 'default' cache will be used instead.
    "cache_name": "versatileimagefield_cache",
    # The save quality of modified JPEG images. More info here:
    # https://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html#jpeg
    # Defaults to 70
    "jpeg_resize_quality": 70,
    # The name of the top-level folder within storage classes to save all
    # sized images. Defaults to '__sized__'
    "sized_directory_name": "__sized__",
    # The name of the directory to save all filtered images within.
    # Defaults to '__filtered__':
    "filtered_directory_name": "__filtered__",
    # The name of the directory to save placeholder images within.
    # Defaults to '__placeholder__':
    "placeholder_directory_name": "__placeholder__",
    # Whether or not to create new images on-the-fly. Set this to `False` for
    # speedy performance but don't forget to 'pre-warm' to ensure they're
    # created and available at the appropriate URL.
    "create_images_on_demand": True,
    # A dot-notated python path string to a function that processes sized
    # image keys. Typically used to md5-ify the 'image key' portion of the
    # filename, giving each a uniform length.
    # `django-versatileimagefield` ships with two post processors:
    # 1. 'versatileimagefield.processors.md5' Returns a full length (32 char)
    #    md5 hash of `image_key`.
    # 2. 'versatileimagefield.processors.md5_16' Returns the first 16 chars
    #    of the 32 character md5 hash of `image_key`.
    # By default, image_keys are unprocessed. To write your own processor,
    # just define a function (that can be imported from your project's
    # python path) that takes a single argument, `image_key` and returns
    # a string.
    "image_key_post_processor": None,
    # Whether to create progressive JPEGs. Read more about progressive JPEGs
    # here: https://optimus.io/support/progressive-jpeg/
    "progressive_jpeg": False,
}

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    "image_gallery": [
        ("gallery_large", "crop__800x450"),
        ("gallery_square_small", "crop__50x50"),
    ],
    "primary_image_detail": [
        ("hero", "crop__600x283"),
        ("social", "thumbnail__800x800"),
    ],
    "primary_image_list": [
        ("list", "crop__400x225"),
    ],
    "headshot": [
        ("headshot_small", "crop__150x175"),
    ],
}
