from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WebCrawler.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^collect/', include('collect.urls')),
    url(r'^crawl/', include('crawl.urls')),
    url(r'', include('collect.urls')),
    url('', include('django_socketio.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
