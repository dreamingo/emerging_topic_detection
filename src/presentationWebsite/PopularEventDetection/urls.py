from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PopularEventDetection.views.home', name='home'),
    # url(r'^PopularEventDetection/', include('PopularEventDetection.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'show.views.home'),
    url(r'^topic', 'show.views.topic'),
    url(r'^related_weibo', 'show.views.related_weibo'),
    url(r'^user_rank$', 'show.views.user_rank'),
    url(r'^analysis', 'show.views.analysis'),

    url(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
