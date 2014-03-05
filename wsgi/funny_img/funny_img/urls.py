from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$','apps.worker.views.index', name='index'),
    url(r'^google/$','apps.worker.views.google', name='google'),
    url(r'^instagram/$','apps.worker.views.instagram', name='instagram'),
    url(r'^admin/', include(admin.site.urls)),
)
