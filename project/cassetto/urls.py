# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

# load admin modules
from django.contrib import admin
admin.autodiscover()

# load api router
from .apps.storage import views as storage_view
# from .apps.sharing import views as storage_view
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'storages', storage_view.StorageViewSet)
router.register(r'resources', storage_view.ResourceViewSet)


urls = (
    url(r'^$', TemplateView.as_view(template_name='base.html')),

    # Examples:
    # url(r'^$', 'cassetto.views.home', name='home'),
    # url(r'^cassetto/', include('cassetto.foo.urls')),

    url(r'^api/v1/', include(router.urls)),
    url(r'^%s/(?P<username>[\w.@+-]+)/(?P<storage>[-a-zA-Z0-9_]+)/(?P<path>.+)' % settings.SENDFILE_URL[1:],
        storage_view.download_view, name='resource-download'),
    # url(r'^api/v1/storages$', storage_view.StorageList.as_view(actions={'get': 'list', 'post': 'create'}), name='storage-list'),
    # url(r'^api/v1/storages/(?P<username>[\w.@+-]+)$', storage_view.StorageList.as_view(actions={'get': 'list', 'post': 'create'}), name='storage-user-list'),
    # url(r'^api/v1/storages/(?P<username>[\w.@+-]+)/(?P<code>[-a-zA-Z0-9_]+)$', storage_view.StorageDetail.as_view(actions={'get': 'retrieve', 'post': 'create'}), name='storage-detail'),
    # url(r'^api/v1/storages/(?P<username>[\w.@+-]+)/(?P<code>[-a-zA-Z0-9_]+)/(?P<path>.+)$', storage_view.ResourceDetail.as_view(actions={'get': 'retrieve', 'post': 'create'}), name='storage-resource-detail'),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns = patterns('', *urls)

# static and media urls not works with DEBUG = True, see static function.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
