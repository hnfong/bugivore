# -*- coding: utf-8 -*-
import unittest
import copy
import random
from string import letters, digits

from django.http import HttpRequest, HttpResponse
from django.template import TemplateSyntaxError

from djangoutils.http.middleware import HTTPStatusMiddleware

# recursively test submodule

test_mods = (
)

test_suite = unittest.TestSuite()
for mod in test_mods:
    test_suite.addTest(doctest.DocTestSuite(mod))
    if hasattr(mod, 'test_suite'):
        test_suite.addTest(mod.test_suite)

# test setup

#
# Need to hack get_current
#
from django.conf import settings
from django.contrib.sites.models import SiteManager, Site
def get_current(self):
    return Site(domain = random_str(), name = random_str())
if not hasattr(settings, 'SITE_ID'):
    SiteManager.get_current = get_current

def middleware():
    return """>>> middleware = HTTPStatusMiddleware()
"""

def random_str(a = 1, b = 100):
    return "".join([ random.choice(letters + digits + '/~._') for i in xrange(random.randint(a, b)) ])

def request(path, method):
    return """>>> request = HttpRequest()
>>> request.path = '%(path)s'
>>> request.method = '%(method)s'
""" % { 'path': path, 'method' : method, }

def random_response(status):
    return """>>> content = random_str(1, 2000)
>>> response = HttpResponse(content)
>>> response.status_code = %(status)s
""" % { 'status': status, }

def setup(status = 200, method = 'GET', path = random_str()):
    return middleware() + request(path, method) + random_response(status)

# some cases

noerror_indent = '...     '

def noerror(expr, result = ''):
    return """>>> try:
%(indent)s%(expr)s
%(indent)s'no error'
... except Exception, e:
%(indent)se
...
%(result)s'no error'
""" % { 'expr': expr, 'result': result, 'indent': noerror_indent }

def samestatus(status = 200, method = 'GET', path = random_str()):
    return setup(status, method, path) + noerror(
        'middleware.process_response(request, response).status_code',
        "%d\n" % status,
    )

def unmodified(status = 200, method = 'GET', path = random_str()):
    return setup(status, method, path) + \
        """>>> middleware.process_response(request, response) == response
True
"""

# tests

__test__ = {
'testProcessResponseUnmodify200: 200 success response should be unmodified GET': unmodified(200, 'GET'),
'testProcessResponseUnmodify200: 200 success response should be unmodified POST': unmodified(200, 'POST'),
'testProcessResponseUnmodify302: 302 redirection response should be unmodified GET': unmodified(302, 'GET'),
'testProcessResponseUnmodify302: 302 redirection response should be unmodified POST': unmodified(302, 'POST'),
'testServerErrorRobust: server_error should not crash on its own GET': setup(500, 'GET') + noerror('res = middleware.server_error(request)'),
'testServerErrorRobust: 404 should give 404 GET': samestatus(404, 'GET'),
'testServerErrorRobust: 404 should give 404 POST': samestatus(404, 'POST'),
'testServerErrorRobust: 403 should give 403 GET': samestatus(403, 'GET'),
'testServerErrorRobust: 404 should give 403 POST': samestatus(403, 'POST'),
'testServerErrorRobust: 500 should give 500 GET': samestatus(500, 'GET'),
'testServerErrorRobust: 500 should give 500 POST': samestatus(500, 'POST'),
'testProcessException: An exception should give 500 GET':
setup(200, 'GET') +
""">>> middleware.process_exception(request, TemplateSyntaxError()).status_code
500
""",
'testProcessException: An exception should give 500 POST':
setup(200, 'POST') +
""">>> middleware.process_exception(request, TemplateSyntaxError()).status_code
500
""",
}
