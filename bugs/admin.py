from django.contrib import admin
from bugivore.bugs.models import *

admin.site.register(Bug)
admin.site.register(Comment)

