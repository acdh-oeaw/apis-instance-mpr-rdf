from apis_acdhch_default_settings.settings import *

DEBUG = False

INSTALLED_APPS += ["apis_highlighter", "django.contrib.postgres",
                   "apis_core.collections", "apis_core.history"]
INSTALLED_APPS.remove("apis_ontology")
INSTALLED_APPS.insert(0, "apis_ontology")

ROOT_URLCONF = 'apis_ontology.urls'

PROJECT_DEFAULT_MD = {}

ALLOWED_HOSTS = ["mpr.acdh-ch-dev.oeaw.ac.at"]

CSRF_TRUSTED_ORIGINS = ["https://mpr.acdh-ch-dev.oeaw.ac.at"]


APIS_LIST_LINKS_TO_EDIT = True


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(name)-6s %(levelname)-8s %(message)s',
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}

LANGUAGE_CODE = "de"

APIS_BASE_URI = "https://mpr.acdh-ch-dev.oeaw.ac.at"
