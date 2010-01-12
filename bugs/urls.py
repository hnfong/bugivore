# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'bugs.views.index'),
    url(r'^new/$', 'bugs.views.new'),
)
