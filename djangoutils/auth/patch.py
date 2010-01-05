# -*- coding: utf-8 -*-
def patch_decorators():
    from django.contrib.auth import decorators
    from djangoutils.auth.decorators import login_required
    decorators.login_required = login_required
