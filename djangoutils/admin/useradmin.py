# -*- coding: utf-8 -*-
# Taken from common/appenginepatch/ragendja/auth/google_admin.py
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from rpx.models import RpxData
class RpxInline(admin.TabularInline):
    model = RpxData

class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'), 'classes': ('collapse',)}),
        (_('Important dates'), {'fields': ('date_joined',)}),
        (_('Groups'), {'fields': ('groups',)}),
    )
    list_display = ('email', 'username', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('user',)
    filter_horizontal = ('user_permissions',)
    inlines = (RpxInline,)
