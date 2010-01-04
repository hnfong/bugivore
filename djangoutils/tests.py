# -*- coding: utf-8 -*-
import unittest
import doctest

import djangoutils.admin.tests
import djangoutils.auth.tests
import djangoutils.http.tests

# recursively test submodule

test_mods = (
    djangoutils.admin.tests,
    djangoutils.auth.tests,
    djangoutils.http.tests,
)

test_suite = unittest.TestSuite()
for mod in test_mods:
   test_suite.addTest(doctest.DocTestSuite(mod))
   if hasattr(mod, 'test_suite'):
       test_suite.addTest(mod.test_suite)
runner = unittest.TextTestRunner()
result = runner.run(test_suite)
