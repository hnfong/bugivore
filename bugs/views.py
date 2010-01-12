# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from ragendja.template import render_to_response

import models

def index(request):
    l = models.Bug.all().fetch(1000)
    return HttpResponse(str( l ))

