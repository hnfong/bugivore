# -*- coding: utf-8 -*-
from django.contrib import admin

from guestbook.forms import GreetingForm
from guestbook.models import Greeting

class GreetingAdmin(admin.ModelAdmin):
    form = GreetingForm

admin.site.register(Greeting, GreetingAdmin)
