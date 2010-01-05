# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from djangoutils.dbutils import auto_cleanup_relations

def _get_full_name(self):
    full_name = None
    if self.first_name or self.last_name:
        full_name = u' '.join([ self.first_name, self.last_name ])
    else:
        full_name = unicode(self.username)
    return full_name.strip()

def patch_user():
    auto_cleanup_relations(User)
    User.get_full_name = _get_full_name

def patch_decorators():
    from django.contrib.auth import decorators
    from djangoutils.auth.decorators import login_required
    decorators.login_required = login_required
