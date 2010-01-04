# -*- coding: utf--8 -*-
import unittest
import doctest

from random import random

from djangoutils import admin
from djangoutils.admin import urlsauto

from django.core.urlresolvers import reverse

# recursively test submodule

test_mods = (
)

test_suite = unittest.TestSuite()
for mod in test_mods:
    test_suite.addTest(doctest.DocTestSuite(mod))
    if hasattr(mod, 'test_suite'):
        test_suite.addTest(mod.test_suite)

# tests

__test__ = {
'Test module working': """
>>> True
True
""",
'Test urlsauto has rootpatterns': """
>>> urlsauto.rootpatterns is None
False
""",
'Test admin.index reversible': """
>>> reverse('admin:index') is None
False
""",
}
