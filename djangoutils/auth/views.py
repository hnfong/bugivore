# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from djangodev.contrib import messages

def login(request, context=None):
    """
    Display the login page for RPX handling.
    """
    context = context or {}
    next = context.pop('next', None) or request.GET.get('next') or getattr(settings, 'LOGOUT_REDIRECT_URL')
    return render_to_response('djangoutils/auth/login.html',
        dict({ 'next': next, }, **context),
        context_instance=RequestContext(request)
    )

def logout(request, context=None):
    if request.method == 'POST':
        context = context or {}
        next = context.pop('next', None) or request.GET.get('next') or getattr(settings, 'LOGOUT_REDIRECT_URL')
        auth.logout(request)
        return HttpResponseRedirect(next)
    else:
        return render_to_response('djangoutils/auth/logout.html',
            context_instance=RequestContext(request))
