# -*- coding: utf-8 -*-

def patch_forms():
    from django import forms
    from djangoutils.forms import models
    forms.save_instance = models.save_instance
    forms.models.save_instance = models.save_instance
