# -*- coding: utf-8 -*-
from django.contrib import admin

from guestbook.models import Greeting

class GreetingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Greeting, GreetingAdmin)
