# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from google.appengine.ext import db


class Bug(db.Model):
    title = db.StringProperty ( required = True )
    user = db.ReferenceProperty( User )
    ctime = db.DateTimeProperty ( required = True, auto_now_add = True )
    content = db.TextProperty ( required = True )
    status = db.StringProperty ( required = True )
    priority = db.IntegerProperty ( required = True )
    assignee = db.ReferenceProperty( User, collection_name='assignee' )

class Comment(db.Model):
    user = db.ReferenceProperty( User )
    bug = db.ReferenceProperty( Bug, required = True )
    ctime = db.DateTimeProperty ( required = True, auto_now_add = True )
    content = db.TextProperty ( required = True )

