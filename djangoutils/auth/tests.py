# -*- coding: utf--8 -*-
import unittest
import doctest

from random import random

#from django.contrib.auth.models import User

from djangoutils import auth
from djangoutils.auth.decorators import *
from djangoutils.auth import urlsauto

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
}

class TestDecorators(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

#def user(username = random(), email = random(), first_name = random(), last_name = random(), active = True,
#authenticated = True, staff = False, superuser = False):
#    return """>>> user = User(username = '%(username)s',
#... email = '%(email)s')
#>>> user.first_name = '%(first_name)s'
#>>> user.last_name = '%(last_name)s'
#>>> user.is_active = %(active)s
#>>> user.is_authenticated = %(authenticated)s
#>>> user.is_staff = %(staff)s
#>>> user.is_superuser = %(superuser)s
#""" % { 'username': username, 'email': email,
#'first_name': first_name, 'last_name': last_name, 
#'active': str(active), 'authenticated': str(authenticated),
#'staff': str(staff), 'superuser': str(superuser), }

#noerror_indent = '...     '

#def noerror(expr, result = ''):
#    return """>>> try:
#%(indent)s%(expr)s
#%(indent)s'no error'
#... except Exception, e:
#%(indent)se
#...
#%(result)s'no error'
#""" % { 'expr': expr, 'result': result, 'indent': noerror_indent }

