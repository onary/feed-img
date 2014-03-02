from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','apps.worker.views.index'),
    url(r'^cache$','apps.worker.views.cache_v'),
    url(r'^admin/', include(admin.site.urls)),
)
