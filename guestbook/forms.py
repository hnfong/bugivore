# -*- coding: utf-8 -*-
from django import forms
from django.forms.util import ErrorList
from django.utils.encoding import force_unicode
from google.appengine.ext import db

from guestbook.models import Greeting

class GreetingForm(forms.ModelForm):

    def __init__(self, *args, **kargs):
        super(GreetingForm, self).__init__(*args, **kargs)

        try:
            from wmd import widgets
            self.fields['message'].widget = widgets.WMDEditor()
        except ImportError:
            pass

    def clean_message(self):
        from djangoutils.core.helpers import clean_html
        message = clean_html(self.cleaned_data['message'].strip())
        try:
            message = Greeting.message.validate(message)
        except db.BadValueError, e:
            self._errors['message'] = ErrorList([force_unicode(e)])
        return message

    class Meta:
        model = Greeting
        exclude = ('author', 'date',)
