# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from djangoutils.dbutils import auto_cleanup_relations

def get_full_name(self):
    full_name = None
    if self.first_name or self.last_name:
        full_name = u' '.join([ self.first_name, self.last_name ])
    else:
        full_name = unicode(self.username)
    return full_name.strip()

def _patch_user():
    import inspect
    import logging

    logging.debug('%s: patching User for auto_cleanup_relations and get_full_name' % inspect.getfile(inspect.currentframe()))
    auto_cleanup_relations(User)
    User.get_full_name = get_full_name

_patch_user()
