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

# Your RPX API key acquired from rpx.com
RPXNOW_API_KEY = 'add your key here'

# Your part of the trustroot, e.g. site in site.rpxnow.com if you are using the
# free service.
RPXNOW_REALM = 'add your realm here'

# List of trusted Open ID providers. If listed here, the email address associated
# by the authenticated user will be used to search for existing users an map the
# two together.
RPX_TRUSTED_PROVIDERS = ('Google',)

# Sets the log level for the RPX backend
RPX_LOG_LEVEL = logging.ERROR

# due to possible initialization order issues, we do not import from django.conf.settings
# instead directly get the specific settings from (project)/settings_overrides.py
try:
    import settings_overrides

    try:
        RPXNOW_API_KEY = settings_overrides.RPXNOW_API_KEY
    except AttributeError:
        pass

    try:
        RPXNOW_REALM = settings_overrides.RPXNOW_REALM
    except AttributeError:
        pass

    try:
        RPX_TRUSTED_PROVIDERS = settings_overrides.RPX_TRUSTED_PROVIDERS
    except AttributeError:
        pass

except ImportError:
    pass

