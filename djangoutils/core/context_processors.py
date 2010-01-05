# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site

def site(request):
    "Returns current sitename"
    current_site = Site.objects.get_current()
    return {
        'domain': current_site.domain,
        'sitename': current_site.name,
    }

def debug(request):
    "Returns context variables helpful for debugging."
    context_extras = {}
    from django.conf import settings
    if getattr(settings, 'DEBUG'):
        context_extras['debug'] = True
    return context_extras

def ip_address(request):
    "Returns IP address"
    return {
        'ip_address': request.META.get('REMOTE_ADDR'),
    }
