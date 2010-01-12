# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from guestbook import views

urlpatterns = patterns('',
    url(r'^$', 'bugs.views.index'),
)
