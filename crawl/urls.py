from django.conf.urls import patterns, url

from crawl import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^status$', views.status, name='status'),
    url(r'^stop$', views.stop, name='stop'),
)