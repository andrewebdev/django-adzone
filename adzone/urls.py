from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<model>[\w]+)/(?P<id>[\d]+)$', 'adzone.views.adView'),
)
