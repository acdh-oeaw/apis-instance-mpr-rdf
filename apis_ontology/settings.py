from apis_acdhch_default_settings.settings import *

DEBUG = False

INSTALLED_APPS += ["django.contrib.postgres", "apis_core.collections", "apis_core.history"]
INSTALLED_APPS.remove("apis_ontology")
INSTALLED_APPS.insert(0, "apis_ontology")

ROOT_URLCONF = 'apis_ontology.urls'

CSRF_TRUSTED_ORIGINS = ["https://mpr.acdh-ch-dev.oeaw.ac.at"]


LANGUAGE_CODE = "de"
