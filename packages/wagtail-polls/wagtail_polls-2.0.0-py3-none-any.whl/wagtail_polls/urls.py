from django.conf.urls import include, url
from django.contrib import admin

from wagtail.core import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls


urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^polls/', include('polls.urls')),
]
