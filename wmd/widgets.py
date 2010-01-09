# -*- coding: utf-8 -*-
# 
# Code by T. Stone
# http://stackoverflow.com/questions/479837/how-can-i-hook-up-wmd-editor-on-my-django-forms/1529258#1529258
from django import forms
from django.conf import settings
from django.template import loader, Context
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode

class WMDEditor(forms.Textarea):
    def render(self, name, value, attrs=None):
        # Prepare values
        if not value:
            value = ''
        attrs = self.build_attrs(attrs, name=name)

        # Render widget to HTML
        t = loader.get_template('wmd/widget.html')
        c = Context({
            'attributes' : forms.util.flatatt(attrs),
            'value' : conditional_escape(force_unicode(value)),
            'id' : attrs['id'],
            'MEDIA_URL': settings.MEDIA_URL,
        })

        return t.render(c)
