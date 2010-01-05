# -*- coding: utf-8 -*-
# Code from django.contrib.auth.decorators
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.utils.http import urlquote

from functools import wraps

from djangodev.contrib import messages

def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME, request_processor=None):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    if not login_url:
        from django.conf import settings
        login_url = getattr(settings, 'LOGIN_URL')
    def decorate(view_func):
        def _pass_wrapper(request, *ags, **kags):
            if request_processor:
                request = request_processor(request)
            if test_func(request.user):
                return view_func(request, *ags, **kags)
            if hasattr(request, 'login_message'):
                messages.error(request, request.login_message)
            tup = login_url, redirect_field_name, request.path
            return HttpResponseRedirect('%s?%s=%s' % tup)
        return wraps(view_func)(_pass_wrapper)
    return decorate


def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME,
        request_processor=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        redirect_field_name=redirect_field_name,
        request_processor=request_processor,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def restricted(test_func=None, error_url=None, request_processor=None):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the error page otherwise. The test should be a callable that
    takes the user object and returns True if the user passes.
    """
    def decorate(view_func):
        @login_required(request_processor=request_processor)
        def _restricted_wrapper(request, *ags, **kags):
            if test_func(request.user):
                return view_func(request, *ags, **kags)
            if hasattr(request, 'restriction_message'):
                messages.error(request, request.restriction_message)
            if error_url:
                return HttpResponseRedirect(error_url)
            return HttpResponseForbidden()
        return wraps(view_func)(_restricted_wrapper)
    return decorate


def active_user_required(function=None, error_url=None, request_processor=None):
    """
    Decorator for views that checks that the user is active, redirecting to the
    an error page otherwise.
    """
    if not error_url:
        from django.conf import settings
        error_url = getattr(settings, 'DISABLED_URL')
    actual_decorator = restricted(
        lambda u: u.is_active,
        error_url=error_url,
        request_processor=request_processor,
    )   
    if function:
        return actual_decorator(function)
    return actual_decorator


def staff_only(function=None, error_url=None, request_processor=None):
    """
    Decorator for views that checks that the user is a staff, showing a
    forbidden message otherwise.
    """
    actual_decorator = restricted(
        lambda u: u.is_staff,
        error_url=error_url,
        request_processor=request_processor,
    )   
    if function:
        return actual_decorator(function)
    return actual_decorator


def active_staff_only(function=None, not_staff_url=None, not_active_url=None,
        request_processor=None):
    """
    Decorator for views that checks that the user is an active staff, showing
    a forbidden message or an error page otherwise.
    """
    def decorate(function):
        return active_user_required(staff_only(function, not_staff_url),
            not_active_url, request_processor)
    if function:
        return decorate(function)
    return decorate
