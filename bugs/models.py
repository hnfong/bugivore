# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from google.appengine.ext import db


class Bug(db.Model):
    title = db.StringProperty ( required = True )
    user = db.UserProperty() # stub, find out how to mess with rpx later
    ctime = db.DateTimeProperty ( required = True, auto_now_add = True )
    content = db.TextProperty ( required = True )
    status = db.StringProperty ( required = True )
    priority = db.IntegerProperty ( required = True )
    assignee = db.UserProperty() # stub.

class Comment(db.Model):
    user = db.UserProperty() # stub, as above.
    bug = db.ReferenceProperty( Bug, required = True )
    ctime = db.DateTimeProperty ( required = True, auto_now_add = True )
    content = db.TextProperty ( required = True )

