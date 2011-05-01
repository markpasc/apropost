from django.conf.urls.defaults import *


urlpatterns = patterns('apropost.views',
    url(r'^$', 'root', name='root'),
    url(r'^register$', 'register', name='register'),
    url(r'^home$', 'home', name='home'),

    url(r'^subscribe$', 'add_subscription', name='subscribe'),
)
