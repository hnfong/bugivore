# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from djangoutils.auth.decorators import active_staff_only

from djangodev.contrib import messages

def patch_admin():
    from django.conf import settings
    ADMIN = 'django.contrib.admin'

    if ADMIN in getattr(settings, 'INSTALLED_APPS'):
        from django.contrib.admin import site

        def add_message(request):
            request.login_message = 'Login required to use the administration interface.'
            request.restriction_message = 'Only staff can use the administration interface.'
            return request

        # function for overriding AdminSite.get_urls() so as to (1) remove
        # password_change and (2) apply custom staff_only decorator
        def get_urls():
            from django.conf.urls.defaults import patterns, url, include

            wrap = active_staff_only(request_processor=add_message)

            # Admin-site-wide views.
            urlpatterns = patterns('',
                url(r'^$',
                    wrap(site.index),
                    name='index'),
                url(r'^logout/$',
                    wrap(site.logout),
                    name='logout'),
                url(r'^jsi18n/$',
                    wrap(site.i18n_javascript),
                    name='jsi18n'),
                url(r'^r/(?P<content_type_id>\d+)/(?P<object_id>.+)/$',
                    'django.views.defaults.shortcut'),
                url(r'^(?P<app_label>\w+)/$',
                    wrap(site.app_index),
                    name='app_list')
            )

            # Add in each model's views.
            for model, model_admin in site._registry.iteritems():
                urlpatterns += patterns('',
                    url(r'^%s/%s/' % (model._meta.app_label, model._meta.module_name),
                        include(model_admin.urls))
                )
            return urlpatterns

        site.get_urls = get_urls
        site.password_change = None
        site.password_change_done = None

        import inspect
        import logging

        logging.debug('%s: \'%s\' patched.' % (
            inspect.getfile(inspect.currentframe()), ADMIN
        ))
