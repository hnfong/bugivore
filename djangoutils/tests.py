# -*- coding: utf-8 -*-
import unittest
import doctest

# apply appropriate patching, to simulate the production environment
import main

def random_str(a = 1, b = 100, charset = None):
    """
    Output a random string of random length between a and b (both inclusive)
    consisting of characters from charset. Useful for generating random test
    strings (e.g. random URL, random content in response).

    Default charset is letters + digits + '/~.-_'.
    """
    from random import random, choice, randint
    if not charset:
        from string import letters, digits
        charset = letters + digits + '/~.-_'
    return "".join([ choice(charset) for i in xrange(randint(a, b)) ])

def setup_test_site():
    """
    If SITE_ID is not set in settings, some tests may fail due to exception
    ImproperlyConfigured, when trying to get the current site object via
    Site.objects.get_current(). A workaround is to output a random site object
    (having a random domain and a random name) in such case.
    """
    from django.conf import settings
    from django.contrib.sites.models import SiteManager, Site
    orig_get_current = SiteManager.get_current
    def get_current(self):
        return Site(domain = random_str(), name = random_str())
    if not hasattr(settings, 'SITE_ID'):
        SiteManager.get_current = get_current
    return orig_get_current

def reset_test_site(get_current):
    """
    Reset Site.objects.get_current(). See setup_test_site().
    """
    from django.contrib.sites.models import SiteManager, Site
    SiteManager.get_current = get_current

# recursively test submodule

import djangoutils.admin.tests
import djangoutils.auth.tests
import djangoutils.db.tests
import djangoutils.http.tests

test_mods = (
    djangoutils.admin.tests,
    djangoutils.auth.tests,
    djangoutils.db.tests,
    djangoutils.http.tests,
)

test_suite = unittest.TestSuite()
for mod in test_mods:
   test_suite.addTest(doctest.DocTestSuite(mod))
   if hasattr(mod, 'test_suite'):
       test_suite.addTest(mod.test_suite)
runner = unittest.TextTestRunner()
result = runner.run(test_suite)
