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

from django.contrib.auth.models import User
from google.appengine.ext import db
from ragendja import dbutils

from rpx.models import RpxData
from rpx.api import RpxApi
from rpx.api import RpxAuthInfo
from rpx import settings

import logging

TRUSTED_PROVIDERS=set(getattr(settings,'RPX_TRUSTED_PROVIDERS', []))

class RpxBackend:
    """Implements an authentication backend that uses RPX to authenticate users."""
    def __init__(self):
        self.logger = logging.getLogger('rpx')
        self.logger.setLevel(settings.RPX_LOG_LEVEL)
        self.api = RpxApi()
    
    def authenticate(self, token=''):
        """Required method for authentication backends."""
        auth_info = self.api.get_auth_info(token)
        
        if not auth_info:
            self.logger.error("RpxBackend: failed to get RPX info for token: " + token)
            return None
                
        return self.get_or_create_user(auth_info)   
    
    
    def get_user(self, id):    
        """Required method for authentication backends. """
        if not id:
            raise ValueError
        
        try: 
            return User.get(id) # Returns None if not found
        except db.KindError:
            self.logger.error('RpxBackend: Entity with ID ' + str(id) + ' id was not of type User!')
            return None
        except db.BadKeyError:
            self.logger.error('RpxBackend: Id ' + str(id) + ' seems malformed')
            return None
    
    
    def create_rpx_key(self, rpx_id):
        """Creates RPX Key from rpx_id.
        
        Adds "key:" prefix as suggested by
        http://code.google.com/appengine/docs/python/datastore/modelclass.html#Model
        """
        if not rpx_id:
            raise ValueError
        return dbutils.generate_key_name(rpx_id)
    
    def create_user(self, rpx_auth_info):
        """Creates user based on the RPX authentication info."""
        username = rpx_auth_info.get_user_name()

        user = dbutils.db_create(User, username=username, email=rpx_auth_info.get_email())
        if not user:
            raise Exception('Cannot create user (name = %s)' % username)
        self.logger.debug("RpxBackend: Created user(%s) as %s\r\n" % (user.username, str(user)))
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.set_unusable_password()
        user.save()
        rpxdata = RpxData(key_name=self.create_rpx_key(rpx_auth_info.get_rpx_id()), user=user)
        rpxdata.save()
        self.logger.debug("RpxBackend: RpxData created\r\n")

        return user
        
    def delete_user(self, user):
        """Deletes user and any associated RPX IDs."""
        if not user or user.__class__ != User:
            raise ValueError
        
        self.logger.debug("RpxBackend: User " + user.username + " will be deleted\r\n")
        user.delete()
        # try to rely on auto_cleanup
        
        self.logger.debug("RpxBackend: User deleted\r\n")
                
    def get_user_by_rpx_id(self, rpx_id):
        """Returns user using the RPX ID."""
        if not rpx_id:
            raise ValueError
        
        rpxData = RpxData.get_by_key_name(self.create_rpx_key(rpx_id)) # Returns None if not found

        if (rpxData):
            return rpxData.user
        else:
            return None
        
    
    def map_to_existing_user_by_email(self, auth_info):
        """Map open ID to existing user based on email.
        
        The open Id provider needs to be in the TRUSTED_PROVIDERS
        list to be able to do this mapping.
        """
        if not auth_info or auth_info.__class__ != RpxAuthInfo:
            raise ValueError
        
        user = None
        
        if auth_info.get_provider() in TRUSTED_PROVIDERS:
            
            user_candidates = dbutils.get_object_list(User, 'email = ', auth_info.get_email())
  
            if user_candidates.count() == 1:
                users = user_candidates.fetch(1)
                user = users[0]
                rpxdata = RpxData(key_name=self.create_rpx_key(auth_info.get_rpx_id()), user=user)
                self.logger.info("RpxBackend: New RPX id for existing user: " + user.username)
        
        return user
    
    def get_or_create_user(self, auth_info):
        """Returns existing user or create new user.
        
        Based on the information in auth_info, this func either retuns an existing user,
        mapps a new open ID to an existing user and returns that user, or creates and
        returns a new user.
        """
        if not auth_info or auth_info.__class__ <> RpxAuthInfo:
            raise ValueError
        
        # Try to get user from RPX ID
        user = self.get_user_by_rpx_id(auth_info.get_rpx_id())

        # Map to existing user email if trusted provider
        if not user:
            user = self.map_to_existing_user_by_email(auth_info)

        # New user, create
        if not user:
            user = self.create_user(auth_info)
        
        return user
    
    def map_id_to_existing_user(self, token, user):
        """Map existing user to new open ID.

        This function should be used to add new open IDs to users that already
        are authenticated.
        
        """
        if not token and not user:
            raise ValueError
        
        auth_info = api.get_auth_info(token)
        
        if auth_info.get_status() == RpxAuthInfo.OK:
            
            # Make sure that this id isn't used
            existing_user = self.get_user_by_rpx_id(auth_info.get_rpx_id())
            
            if not existing_user:
                rpxdata = RpxData(key_name=self.create_rpx_key(auth_info.get_rpx_id()), user=user)
                rpxdata.save()
