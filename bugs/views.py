# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.views.generic.create_update import create_object
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from ragendja.template import render_to_response

from bugs import models

def index(request):
    l = models.Bug.all().fetch(1000)
    return HttpResponse(str( l ))

# See http://code.google.com/appengine/articles/app-engine-patch.html
def new(request):
    request.POST = request.POST.copy()
    request.POST['author'] = str(request.user.key())
    return create_object(request, models.Bug, post_save_redirect=reverse('bugs.views.index'), template_name='bugs/new.html')
