# -*- coding: utf-8 -*-
def patch_django():
    from djangoutils.admin.patch import patch_admin
    patch_admin()

    from djangoutils.auth.patch import patch_decorators
    patch_decorators()

    from djangoutils.db.patch import patch_db
    patch_db()

    from djangoutils.http.patch import patch_debug
    patch_debug()
