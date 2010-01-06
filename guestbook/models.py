# -*- coding: utf-8 -*-
from google.appengine.ext import db
from django.contrib.auth.models import User

from djangoutils.core.helpers import truncate

class Greeting(db.Model):
    author = db.ReferenceProperty(User)
    content = db.StringProperty(multiline = True)
    date = db.DateTimeProperty(auto_now_add = True)

    def __unicode__(self):
        return self.author.username + '   ' + truncate(self.content, 50)
