# -*- coding: utf-8 -*-
from google.appengine.ext import db
from django.contrib.auth.models import User
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _

def max_length(message):
    if len(message) > 500:
        raise db.BadValueError, '%s cannot be longer than 500 characters (length is %d).' % (
            force_unicode(Greeting.message.verbose_name), len(message) )
    return message

class Greeting(db.Model):
    author = db.ReferenceProperty(User, verbose_name=_('Author'))
    message = db.StringProperty(multiline=True, verbose_name=_('Message'), validator=max_length)
    date = db.DateTimeProperty(auto_now_add = True, verbose_name=_('Date and Time'))

    def __unicode__(self):
        from django.utils.html import strip_tags
        from djangoutils.core.helpers import truncate
        return self.author.username + '   ' + truncate(strip_tags(self.message), 50)
