# -*- coding: utf-8 -*-
# Based on ragendja ErrorMiddleware

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

# TODO: more testing for extreme robustness
# TODO: when confident with error handling, write a form to receive feedback

class HTTPStatusMiddleware(object):
    """
    Custom handling of 403, 404, 500, etc.
    """
    def process_exception(self, request, exception):
        try:
            if isinstance(exception, CapabilityDisabledError):
                return self.maintenence(request, exception)
            return self.server_error(request, exception)
        except Exception, e:
            return self.server_error(request, e)

    def process_response(self, request, response):
        status = response.status_code
        if status < 400: # optimize for common cases
            return response

        try:
            if status in ( 403, 404, 500, ):
                request.response = response.content
                return self.fetch_page(request, status)
        except Exception, e:
            if status <> 500: # otherwise, serving 500 raises exception
                return self.server_error(request, e)

        return response

    def maintenence(self, request, *args, **kwargs):
        return render_to_response('maintenance.html', request = request)

    def server_error(self, request, exception = None, *args, **kwargs):
        """
        Graceful degradation, last resort.

        usage:
            server_error(request, [ exception = None])
        """
        try:
            import logging
            logging.exception('server error')
        except:
            pass

        try: # render default 500 response
            from django.conf import settings
            debugkey = request.REQUEST.get('debugkey')
            DEBUG = getattr(settings, 'DEBUG')

            if DEBUG or (debugkey and debugkey == getattr(settings, 'DEBUGKEY')):
                import sys
                from django.views import debug
                return debug.technical_500_response(request, *sys.exc_info())
        except:
            pass

        try: # try coustom response
            if exception:
                request.response = str(exception)
            return self.fetch_page(request, 500)
        except:
            pass

# TODO: More detailed report from a static file
        response = http.HttpResponse("Server error: we are having a big trouble, or otherwise you wouldn't see this.")
        response.status_code = 500
        return response

    def fetch_page(self, request, status):
        """
        Fetch a customized page for handling HTTP status

        usage:
            fetcha_page(request, status)
        """
        response = render_to_response(str(status) + '.html', context_instance=RequestContext(request))
        response.status_code = status
        return response
