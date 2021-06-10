import os

import dj_database_url

from tests.settings import *  # noqa

DATABASES = {"default": dj_database_url.config(conn_max_age=600, ssl_require=True)}

ALLOWED_HOSTS = [".herokuapp.com"]

SECRET_KEY = os.environ["SECRET_KEY"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
] + MIDDLEWARE  # noqa

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(PROJECT_DIR, "../", "staticfiles")  # noqa

DEBUG = False
