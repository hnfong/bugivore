# -*- coding: utf-8 -*-
from django.utils.translation import string_concat
from django.contrib.auth.models import User
from djangoutils.db.dbutils import auto_cleanup_relations
from google.appengine.ext import db

def _get_full_name(self):
    full_name = None
    if self.first_name or self.last_name:
        full_name = u' '.join([ self.first_name, self.last_name ])
    else:
        full_name = unicode(self.username)
    return full_name.strip()

def _get_key_for(self, prop_name):
    return getattr(self.__class__, prop_name).get_value_for_datastore(self)

def _patch_user():
    auto_cleanup_relations(User)
    User.get_full_name = _get_full_name

def _patch_model():
    db.Model.get_key_for = _get_key_for

def patch_db():
    _patch_user()
    _patch_model()
