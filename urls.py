# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from ragendja.urlsauto import urlpatterns

handler500 = 'ragendja.views.server_error'

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template',
        {'template': 'main.html'}, name='frontpage'),
) + urlpatterns
