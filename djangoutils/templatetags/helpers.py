# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter

from djangoutils.core import helpers

register = template.Library()

truncate = register.filter(stringfilter(helpers.truncate))
