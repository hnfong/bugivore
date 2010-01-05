# Copyright (c) 2009, Benny Bergsell
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or 
# without modification, are permitted provided that the following 
# conditions are met:
#
#    * Redistributions of source code must retain the above copyright 
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in 
#      the documentation and/or other materials provided with the 
#      distribution.
#    * Neither the name of the <ORGANIZATION> nor the names of its 
#      contributors may be used to endorse or promote products derived 
#      from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED 
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS 
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
# THE POSSIBILITY OF SUCH DAMAGE.
#
#
#
#           RPX Authentication Backend for Django running
#            on Google App Engine using App Engine Patch
#
#              http://code.google.com/p/django-gae-rpx/
#
#                  Benny Bergsell, 2009-05-17
#                       bergsell@gmail.com
#
#

import unittest

from google.appengine.ext import db
from django.utils import simplejson
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from ragendja.dbutils import generate_key_name

from rpx.models import RpxData
from rpx.backends import RpxBackend
from rpx.api import RpxAuthInfo

# apply appropriate patching, to simulate the production environment
import main

class TestRpxBackends(unittest.TestCase):
    """Test the functionality offered by backends.py"""
    
    def __create_normal_user__(self):
        """Creates a "normal" user that used in numerous test cases below."""
        
        normalJson = '''
            {
              "profile": {
                "displayName": "brian",
                "preferredUsername": "brian",
                "email": "brian@brian.com",
                "providerName": "Google",
                "identifier": "http:\/\/brian.myopenid.com\/"
              },
              "stat": "ok"
            }'''
            
        json = simplejson.loads(normalJson)
        
        auth_info = RpxAuthInfo(json)
        
        self.assert_(auth_info)
        self.assert_(auth_info.get_status() == RpxAuthInfo.OK)
        
        user = RpxBackend.create_user(self.backend, auth_info)
        
        self.assert_(user)
        self.assert_(user.username == "brian")
        self.assert_(user.email == "brian@brian.com")
        
        return user, auth_info
    
    def setUp(self):
        self.backend = RpxBackend()
        # Need to hack get_current
        from django.conf import settings
        from django.contrib.sites.models import SiteManager, Site
        def get_current(self):
            return Site(domain = 'test.domain.com', name = 'test.site')
        if not hasattr(settings, 'SITE_ID'):
            SiteManager.get_current = get_current
        
    def tearDown(self):
        pass
    
    def testCreateRpxKey(self):
        """Tests create_rpx_key().
        
        create_rpx_key() should make sure that the key name starts with legal characters as defined by 
        http://code.google.com/appengine/docs/python/datastore/modelclass.html#Model
           
        """
        rpx_id = "abcd1234"
        rpx_key = generate_key_name(rpx_id)
        
        self.assert_(RpxBackend.create_rpx_key(self.backend, rpx_id) == rpx_key)
        
        try:
            RpxBackend.create_rpx_key(self.backend, None)
            self.assert_(False)
        except:
            pass
        
    def testCreateNewUser(self):
        """Tests RpxBackend.create_user().
        
        Creates a new normal user.
        
        """
        user, auth_info = self.__create_normal_user__()
        
        retreived_user = RpxBackend.get_user_by_rpx_id(self.backend, auth_info.get_rpx_id())
        
        self.assert_(retreived_user == user)        
        self.assert_(user.key() == retreived_user.key())
        
        RpxBackend.delete_user(self.backend, user)

    def testCreateNewUserWithExistingUsername(self):

        user, auth_info = self.__create_normal_user__()
        
        testJson2 = '''
            {
              "profile": {
                "displayName": "brian",
                "preferredUsername": "brian",
                "email": "brian@brian2.com",
                "providerName": "Other",
                "identifier": "http:\/\/brian2.myopenid.com\/"
              },
              "stat": "ok"
            }'''

        json = simplejson.loads(testJson2)
        
        auth_info = RpxAuthInfo(json)

        user2 = RpxBackend.create_user(self.backend, auth_info)

        self.assert_(user2)
        self.assert_(user2.username == "brian")
        self.assert_(user2.email == "brian@brian2.com")
        
        RpxBackend.delete_user(self.backend, user)
        RpxBackend.delete_user(self.backend, user2)
        
    def testDeleteUser(self):
        """Tests RpxBackend.delete_user().
        
        Tests that both the user and the associated RPX data entries are deleted.
        
        """
        user, auth_info = self.__create_normal_user__()
        
        user_key = user.key()
        
        number_of_users_entries = User.all().count()
        number_of_rpx_entries = RpxData.all().count()
        
        RpxBackend.delete_user(self.backend, user)
        
        self.assert_(User.all().count() == number_of_users_entries - 1)
        self.assert_(RpxData.all().count() == number_of_rpx_entries - 1)
        self.assert_(RpxBackend.get_user(self.backend, user_key) == None)
        
    
    def testDeleteNoneUser(self):
        """Tests RpxBackend.delete_user().
        
        Make sure that delete_user can handle None and that it only deletes Users!
        """
        try:
            RpxBackend.delete_user(self.backend, None)
            self.assert_(False)
        except ValueError:
            pass
        
        try:
            RpxBackend.delete_user(self.backend, "stringObject")
            self.assert_(False)
        except ValueError:
            pass
        
    def testGetUserFromRpxId(self):
        """Tests RpxBackend.get_user_by_rpx_id()."""
        
        user, auth_info = self.__create_normal_user__()
        
        self.assert_(user == RpxBackend.get_user_by_rpx_id(self.backend, auth_info.get_rpx_id()))
        
        RpxBackend.delete_user(self.backend, user)
        
    def testGetUserFromNoneRpxId(self):
        """Tests RpxBackend.get_user_by_rpx_id().
        
        Make sure it handles None and negative results.
        
        """
        try:
            RpxBackend.get_user_by_rpx_id(self.backend, None)
            self.assert_(False)
        except ValueError:
            pass
        
        self.assert_(RpxBackend.get_user_by_rpx_id(self.backend, "will not find") == None)
        
    def testGetUserFromRpxIdWithInvalidModel(self):
        
        try:
            rpx_data = RpxData(key_name=RpxBackend.create_rpx_key(self.backend, "thisiskey"), user=None)
            self.assert_(False)
        except db.BadValueError:
            pass            
        
        self.assert_(RpxBackend.get_user_by_rpx_id(self.backend, "thisiskey") == None)
        
    def testGetUserFromId(self):
        """Tests RpxBackend.get_user().
        
        Make sure it handles None and negative results.
        
        """
        
        try:
            RpxBackend.get_user(self.backend, None)
            self.assert_(False)
        except:
            pass
        
        self.assert_(RpxBackend.get_user(self.backend, "willnotfind") == None)
        
        user = User(username="james")
        user.save()
        rpx_data = RpxData(user=user)
        rpx_data.save()
        
        #Test that is can handle key from non User class and returns None
        self.assert_(RpxBackend.get_user(self.backend, rpx_data.key()) == None)
        
        RpxBackend.delete_user(self.backend, user)
          
    def testMapRpxIdToExistingUser(self):
        """Tests RpxBackend.map_to_existing_user_by_email().
        
        This function should be able to map existing user to new RPX id's by
        matching email addresses from trusted providers.
        
        """
        user, auth_info = self.__create_normal_user__()
        
        testJson2 = '''
            {
              "profile": {
                "displayName": "brian",
                "preferredUsername": "brian",
                "email": "brian@brian.com",
                "providerName": "Google",
                "identifier": "http:\/\/brian.anotheropenid.com\/"
              },
              "stat": "ok"
            }'''
            
        json = simplejson.loads(testJson2)
        
        auth_info = RpxAuthInfo(json)        
        
        self.assert_(auth_info)
        self.assert_(auth_info.get_status() == RpxAuthInfo.OK)       
        
        user2 = RpxBackend.map_to_existing_user_by_email(self.backend, auth_info)
        
        self.assert_(user == user2)
        
        RpxBackend.delete_user(self.backend, user)

    def testMapNoneRpxIdToExistingUser(self):
        """Tests error cases for RpxBackend.map_to_existing_user_by_email()."""
        
        try:
            RpxBackend.map_to_existing_user_by_email(self.backend, None)
            self.assert_(False)
        except ValueError:
            pass
        
        try:
            self.assert_(RpxBackend.map_to_existing_user_by_email(self.backend, "StringObject") == None)
            self.assert_(False)
        except ValueError:
            pass
        
        
    def testGetOrCreateUser(self):
        """Tests RpXBackend.get_or_create_user()."""
        
        try:
            RpxBackend.get_or_create_user(self.backend, None)
            self.assert_(False)
        except ValueError:
            pass
        
        user, auth_info = self.__create_normal_user__()
        
        self.assert_(user == RpxBackend.get_or_create_user(self.backend, auth_info))
        
        testJson2 = '''
            {
              "profile": {
                "displayName": "brian",
                "preferredUsername": "brian",
                "email": "brian@brian.com",
                "providerName": "Google",
                "identifier": "http:\/\/brian.anotheropenid.com\/"
              },
              "stat": "ok"
            }'''
            
        json = simplejson.loads(testJson2)
        
        auth_info = RpxAuthInfo(json)       
        
        self.assert_(user == RpxBackend.get_or_create_user(self.backend, auth_info))
        
        RpxBackend.delete_user(self.backend, user)
        
        testJson2 = '''
            {
              "profile": {
                "displayName": "james",
                "preferredUsername": "james",
                "email": "james@james.com",
                "providerName": "Google",
                "identifier": "http:\/\/james.openid.com\/"
              },
              "stat": "ok"
            }'''
            
        json = simplejson.loads(testJson2)
        
        auth_info = RpxAuthInfo(json)
        
        new_user = RpxBackend.get_or_create_user(self.backend, auth_info)
        
        self.assert_(new_user)
        self.assert_(new_user.username == "james")

        self.backend.delete_user(new_user)
        

##################################################################################

class TestRpxApi(unittest.TestCase):
    """
    Test cases for the RpxAIP
    """

    def testApiValidJson(self):
        """Tests the RpxAuthInfo constructor.
        
        Should always be possible to create RpxAuthInfo objects. Status should
        be used by applications to decide if the response from RPX was valid.
        
        """
        testJson = '''
            {
              "profile": {
                "displayName": "brian",
                "preferredUsername": "brian",
                "email": "brian@brian.com",
                "providerName": "Other",
                "identifier": "http:\/\/brian.myopenid.com\/"
              },
              "stat": "ok"
            }'''
            
        json = simplejson.loads(testJson)
        
        auth_info = RpxAuthInfo(json)
        self.assert_(auth_info)
        self.assert_(auth_info.get_status() == RpxAuthInfo.OK)
        self.assertEquals(auth_info.get_user_name(), "brian")
        self.assertEquals(auth_info.get_rpx_id(), "http://brian.myopenid.com/")
        self.assertEquals(auth_info.get_email(), "brian@brian.com")
        self.assertEquals(auth_info.get_provider(), "Other")

    def testApiValidJsonWithAltFields(self):
        """Tests that alternative fields for email and user name can be handled."""
        
        testJson = '''
            {
              "profile": {
                "displayName": "brian",
                "verifiedEmail": "brian@brian.com",
                "providerName": "Other",
                "identifier": "http:\/\/brian.myopenid.com\/"
              },
              "stat": "ok"
            }'''

        json = simplejson.loads(testJson)
        
        auth_info = RpxAuthInfo(json)
        self.assert_(auth_info)
        self.assertEquals(auth_info.get_user_name(), "brian")
        self.assertEquals(auth_info.get_rpx_id(), "http://brian.myopenid.com/")
        self.assertEquals(auth_info.get_email(), "brian@brian.com")
        self.assertEquals(auth_info.get_provider(), "Other")
        
    def testApiMissingProfile(self):
        """Tests error case were the 'profile' entry is missing."""
        
        testJson = '''
            {
              "noProfile": {
                "displayName": "something"
              },
              "stat": "ok"
            }'''

        json = simplejson.loads(testJson)
        
        auth_info = RpxAuthInfo(json)
        
        self.assert_(auth_info)
        self.assert_(auth_info.get_status() == RpxAuthInfo.MISSING)

    def testApiWrongProfile(self):
        """Tests error case where the 'profile' value is malformed."""
        
        testJson = '''
            {
              "profile": "hello",
              "stat": "ok"
            }'''

        json = simplejson.loads(testJson)
        
        auth_info = RpxAuthInfo(json)
        
        self.assert_(auth_info)
        self.assert_(auth_info.get_status() == RpxAuthInfo.MALFORMED)
        
    def testApiEmptyProfile(self):
        """Tests error case where the 'profile' value is empty."""
        
        testJson = '''
            {
              "profile": "",
              "stat": "ok"
            }'''

        json = simplejson.loads(testJson)
        
        auth_info = RpxAuthInfo(json)
        
        self.assert_(auth_info)
        self.assert_(auth_info.get_status() == RpxAuthInfo.MISSING)

    def testApiNotOk(self):
        """Tests error case where the 'stat' value is not ok."""
        
        testJson = '''
            {
              "noProfile": {
                "displayName": "something"
              },
              "stat": "nok"
            }'''

        json = simplejson.loads(testJson)
        
        auth_info = RpxAuthInfo(json)
        
        self.assert_(auth_info)
        self.assert_(auth_info.get_status() == RpxAuthInfo.ERROR)
        
    def testApiEmpty(self):
        """Tests error case where the Json response is an empty string."""
        
        testJson = ""
        
        #Test simplejson
        try:
            json = simplejson.loads(testJson)
            assert_(False) #simplejson should throw exception!
        except ValueError:
            pass   
        
        #Test constructor
        auth_info = RpxAuthInfo({})
        self.assert_(auth_info)
        self.assert_(auth_info.get_status() == RpxAuthInfo.MISSING)
                
##################################################################################
        
class testRpxData(unittest.TestCase):
    """Tests the RpxData model."""
    
    def setUp(self):
        self.backend = RpxBackend()
    
    def testRequired(self):
        """Test to assert that there is always a user reference."""
        try:
            rpx_data = RpxData()
            self.assert_(False)
        except db.BadValueError:
            pass
        
    def testToString(self):
        """Tests that the __unicode__ function creates a string"""
        
        user = User(username="jim")
        user.save()
        rpx_data = RpxData(user=user)
        rpx_data.save()
        rpx_string = str(rpx_data)
        self.assert_(rpx_string.__class__ == str)
        
        RpxBackend.delete_user(self.backend, user)
        
rpx_backends_suite = unittest.TestLoader().loadTestsFromTestCase(TestRpxBackends)
rpx_api_suite = unittest.TestLoader().loadTestsFromTestCase(TestRpxBackends)
test_suite = unittest.TestSuite([rpx_backends_suite, rpx_api_suite])
