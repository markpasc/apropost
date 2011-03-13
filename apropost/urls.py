from django.conf.urls.defaults import *


urlpatterns = patterns('apropost.views',
    url(r'^$', 'root', name='root'),
    url(r'^home$', 'home', name='home'),
)
