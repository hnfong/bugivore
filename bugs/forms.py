# -*- coding: utf-8 -*-
from django import forms
from django.forms.util import ErrorList
from django.utils.encoding import force_unicode
from google.appengine.ext import db

from bugs import models

class BugForm(forms.ModelForm):
    def __init__(self, *args, **kargs):
        super(BugForm, self).__init__(*args, **kargs)

    class Meta:
        model = models.Bug
        exclude = ('user', )
