# -*- coding: utf-8 -*-
import unittest
from django.http import HttpRequest, HttpResponse
from django.template import TemplateSyntaxError
from djangoutils.tests import random_str, setup_test_site, reset_test_site
from djangoutils.http.middleware import HttpStatusMiddleware

# recursively test submodule

test_mods = (
)

test_suite = unittest.TestSuite()
for mod in test_mods:
    test_suite.addTest(doctest.DocTestSuite(mod))
    if hasattr(mod, 'test_suite'):
        test_suite.addTest(mod.test_suite)

# tests

class TestMiddleware(unittest.TestCase):
    def setUp(self):
        self.get_current = setup_test_site()
        self.middleware = HttpStatusMiddleware()

    def tearDown(self):
        reset_test_site(self.get_current)

    def _random_request(self, path=None, method=None):
        """
        Prepare a random request object with given path and method.

        Default path is random_str() if None is given.
        Default method is 'GET' if None is given.
        """
        request = HttpRequest()
        request.path = path or random_str()
        request.method = method or 'GET'
        return request

    def _random_response(self, status=None, content=None):
        """
        Prepare a random response object with given status and content.

        Default status is 200 is None is given.
        Default content is random_str() if None is given.
        """
        response = HttpResponse(content or random_str())
        response.status_code = status
        return response

    def _random_request_response(self, path=None, method=None, status=None,
            content=None):
        """
        Prepare a pair of random request/response objects. See
        _random_request() and _random_response().
        """
        return self._random_request(path, method), \
            self._random_response(status, content)

    def _assert_process_response_unmodified(self, **kargs):
        """
        Run middleware.process_response on a pair of randomly generated
        request/response objects, and assert that the returned response is
        the original one.
        """
        request, response = self._random_request_response(**kargs)
        new_response = self.middleware.process_response(request, response)
        self.assertEqual(new_response, response)

    def _assert_process_response_same_status(self, **kargs):
        """
        Run middleware.process_response on a pair of randomly generated
        request/response objects, and assert that the returned response has
        the same status as the original one.
        """
        request, response = self._random_request_response(**kargs)
        new_response = self.middleware.process_response(request, response)
        self.assertEqual(new_response.status_code, response.status_code)

    def testProcessResponseUnmodifiedOn200GET(self):
        self._assert_process_response_unmodified(status=200, method='GET')

    def testProcessResponseUnmodifiedOn200POST(self):
        self._assert_process_response_unmodified(status=200, method='POST')

    def testProcessResponseUnmodifiedOn302GET(self):
        self._assert_process_response_unmodified(status=302, method='GET')

    def testProcessResponseUnmodifiedOn302POST(self):
        self._assert_process_response_unmodified(status=302, method='POST')

    def testServerErrorDoesNotCrashOn500GET(self):
        request, response = self._random_request_response(status=500, method='GET')
        self.middleware.server_error(request)

    def testServerErrorDoesNotCrashOn500POST(self):
        request, response = self._random_request_response(status=500, method='POST')
        self.middleware.server_error(request)

    def testProcessResponseSameStatusOn403GET(self):
        self._assert_process_response_same_status(status=403, method='GET')

    def testProcessResponseSameStatusOn403POST(self):
        self._assert_process_response_same_status(status=403, method='POST')

    def testProcessResponseSameStatusOn404GET(self):
        self._assert_process_response_same_status(status=404, method='GET')

    def testProcessResponseSameStatusOn404POST(self):
        self._assert_process_response_same_status(status=404, method='POST')

    def testProcessResponseSameStatusOn500GET(self):
        self._assert_process_response_same_status(status=500, method='GET')

    def testProcessResponseSameStatusOn500POST(self):
        self._assert_process_response_same_status(status=500, method='POST')

    def testProcessExceptionRaise500OnGET(self):
        request = self._random_request(method='GET')
        new_response = self.middleware.process_exception(request, TemplateSyntaxError())
        self.assertEqual(new_response.status_code, 500)

    def testProcessExceptionRaise500OnPOST(self):
        request = self._random_request(method='POST')
        new_response = self.middleware.process_exception(request, TemplateSyntaxError())
        self.assertEqual(new_response.status_code, 500)

test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMiddleware))
