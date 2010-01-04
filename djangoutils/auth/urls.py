from django.conf.urls.defaults import *

from djangoutils.auth import views

urlpatterns = patterns('',
                       url(r'^login/$', views.login, name='djangoutils.auth.views.login'),
                       url(r'^logout/$', views.logout, name='djangoutils.auth.views.logout'),
                       )
