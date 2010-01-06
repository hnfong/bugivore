# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from guestbook import views

urlpatterns = patterns('',
    url(r'^$', 'guestbook.views.list'),
    url(r'^sign/$', 'guestbook.views.sign'),
)
