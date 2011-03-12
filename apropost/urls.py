from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 'apropost.views.home', name='home'),
)
