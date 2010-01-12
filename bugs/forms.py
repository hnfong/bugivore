# -*- coding: utf-8 -*-
from django import forms
from django.forms.util import ErrorList
from django.utils.encoding import force_unicode
from google.appengine.ext import db

from bugs.models import Bug

class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        exclude = ('ctime', )
        # We exclude ctime, because it is added automatically

class BugInputForm(BugForm):
    class Meta:
        model = Bug
        exclude = ('user', 'ctime', )
        # We exclude both ctime and user, because they are added automatically
