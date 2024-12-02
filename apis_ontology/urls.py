from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from apis_acdhch_default_settings.urls import urlpatterns


urlpatterns += staticfiles_urlpatterns()
