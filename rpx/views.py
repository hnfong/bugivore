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

import logging

from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from rpx.api import RpxApi
from rpx import settings

def rpx_login_response(request):
    """Handle the login response from RPX."""
    
    logger = logging.getLogger()
    logger.setLevel(settings.RPX_LOG_LEVEL)
    
    token = request.GET.get('token', '')
    next = request.GET.get('next', '')
    logger.debug("rpx_login_response: Next = " + next)
    
    if not token:
        logger.error("rpx_login_response: No token was present") 
        return HttpResponseForbidden()
    
    user = authenticate(token=token)
    
    if user and user.is_active:
        request.session.save() #@todo: Is this needed?
        login(request, user)
        
        return HttpResponseRedirect(next)
    else:
        logger.error("rpx_login_response: No user or inactive user...")
        return HttpResponseForbidden()        

@login_required        
def rpx_map_response(request):
    """Handle the login response from RPX used to map user with several id's"""
    
    logger = logging.getLogger()
    logger.setLevel(settings.RPX_LOG_LEVEL)
    
    token = request.GET.get('token', '')
    
    if not token:
        logger.error("rpx_login_response: No token was present") 
        return HttpResponseForbidden()
      
    backend = RpxBackend()
    backend.map_to_existing_user(token, request.user)
        
    return HttpResponseRedirect('.')
    