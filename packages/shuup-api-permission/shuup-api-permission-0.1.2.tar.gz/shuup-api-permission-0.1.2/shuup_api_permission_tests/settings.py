# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import tempfile

BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = "xyz"

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "easy_thumbnails",
    "filer",
    "shuup.themes.classic_gray",
    "shuup.core",
    "shuup.admin",
    "shuup.default_tax",
    "shuup.customer_group_pricing",
    "shuup.campaigns",
    "shuup.simple_supplier",
    'shuup.front',
    'shuup.front.apps.auth',
    'shuup.front.apps.customer_information',
    'shuup.front.apps.personal_order_history',
    'shuup.front.apps.saved_carts',
    'shuup.front.apps.registration',
    'shuup.front.apps.simple_order_notification',
    'shuup.front.apps.simple_search',
    "shuup.notify",
    "shuup.regions",
    "shuup.testing",
    "shuup.xtheme",

    # external apps
    "bootstrap3",
    "registration",

    'rest_framework',
    'rest_jwt_permission',
    'shuup_api_permission'
)

MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "shuup.front.middleware.ProblemMiddleware",
    "shuup.front.middleware.ShuupFrontMiddleware",
    "shuup_api_permission.middleware.ShuupAPIPermissionMiddleware"
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(
            tempfile.gettempdir(),
            "shuup_api_permission_tests.sqlite3"
        )
    }
}

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "var", "media")

STATIC_URL = "/static/"

ROOT_URLCONF = "shuup_workbench.urls"

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = "en"

LANGUAGES = (
    ("en", "English"),
)

PARLER_DEFAULT_LANGUAGE_CODE = "en"

PARLER_LANGUAGES = {
    None: [
        {"code": code, "name": name}
        for code, name in LANGUAGES
    ],
    "default": {
        "hide_untranslated": False
    }
}

SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"

_TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
]

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": ".jinja",
            "context_processors": _TEMPLATE_CONTEXT_PROCESSORS,
            "newstyle_gettext": True,
            "environment": "shuup.xtheme.engine.XthemeEnvironment",
        },
        "NAME": "jinja2",
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": _TEMPLATE_CONTEXT_PROCESSORS,
            "debug": True
        }
    }
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'shuup_api_permission.authentication.APITokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'shuup_api_permission.permissions.APIAccessPermission',
        'shuup_api_permission.permissions.APIScopePermission'
    )
}

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_PAYLOAD_HANDLER': 'shuup_api_permission.utils.jwt_payload_handler'
}
