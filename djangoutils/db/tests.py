# -*- coding: utf--8 -*-
import unittest
import doctest

from random import random

from google.appengine.ext import db
from djangoutils.db.dbutils import auto_cleanup_relations

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
}
