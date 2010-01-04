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

import urllib
import urllib2

from django.utils import simplejson
from django.contrib.auth.models import User

from rpx.models import RpxData
from rpx import settings

class RpxAuthInfo:
    """
    Represents the decoded user authentication information. 
    
    Assumptions:
    
    Besides 'stat' and 'profile', the fields 'identifier' and 'providerName'
    are assumed to be mandatory.
           
    @todo: Too much logic in constructor? Consider other pattern for creating objects
           of this class?
    
    """
    OK = 1         
    ERROR = 2       # RPX returned an error
    MALFORMED = 3   # JSON has structure errors
    MISSING = 4     # Mandatory fields are missing
    
    def __init__(self, json):
        
        self.rpx_id = None
        self.user_name = None
        self.email = None
        self.provider = None
        self.status = self.ERROR
        
        try:
            if json['stat'] == 'ok':

                self.status = self.OK
                
                profile = json['profile']
                
                if profile:
                    #Mandatory
                    self.rpx_id = profile['identifier']
                    self.provider = profile.get("providerName")

                    if profile.has_key('verifiedEmail'):
                        self.email = profile.get('verifiedEmail') 
                    elif profile.has_key('email'):
                        self.email = profile.get('email')
                    
                    if profile.has_key('preferredUsername'):
                        self.user_name = profile.get('preferredUsername') 
                    elif profile.has_key('displayName'):
                        #@todo: Create user name from display name!
                        self.user_name = profile.get('displayName')
                    else:
                        #@todo: Create user name from email
                        pass  
                
                else:
                    self.status = self.MISSING
        except KeyError:
            # Will catch all missing mandatory keys like 'stat', 'profile', 'identifier', 'providerName',
            # and if 'profile' is malformed
            self.status = self.MISSING

        except TypeError:
            # Will catch problems like e.g. if the 'profile' isn't formatted correctly
            self.status = self.MALFORMED
        
    def get_rpx_id(self):
        """Returns RPX ID.
        
        Client should check status with get_status() to make sure that the field is valid.
        
        """
        return self.rpx_id
    
    def get_user_name(self):
        """Returns user name.
        
        Client should check status with get_status() to make sure that the field is valid.
        
        """
        return self.user_name
    
    def get_email(self):
        """Returns email.
        
        Client should check status with get_status() to make sure that the field is valid.
        
        """
        return self.email
    
    def get_provider(self):
        """Returns provider.
        
        Client should check status with get_status() to make sure that the field is valid.
        
        """
        return self.provider
    
    def get_status(self):
        """Returns the authentication status.
        
        Clients must use get_status() to handle error cases properly.
        
        """
        return self.status

class RpxApi:
    """
    A representation of the RpxApi. Implements the get auth info
    """

    def get_auth_info(self, token=''):
        """
        Used for getting a new identifier
        Arguments:
        - `self`: this object
        - `token`: a token to be parsed by token_url
        """
        url = 'https://rpxnow.com/api/v2/auth_info'
        args = {
          'format': 'json',
          'apiKey': settings.RPXNOW_API_KEY,
          'token': token
        }
        r = urllib2.urlopen(url=url,
          data=urllib.urlencode(args),
        )
        
        json = simplejson.load(r)
        
        return RpxAuthInfo(json)