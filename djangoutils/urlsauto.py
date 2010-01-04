# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from djangoutils.admin.urlsauto import rootpatterns as admin_root
from djangoutils.auth.urlsauto import rootpatterns as auth_root

rootpatterns = admin_root + auth_root
