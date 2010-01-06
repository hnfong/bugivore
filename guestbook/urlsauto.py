# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

appname = 'guestbook'

rootpatterns = patterns('',
    (r'^' + appname + '/', include(appname + '.urls')),
)
