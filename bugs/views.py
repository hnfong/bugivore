# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from bugs.models import Bug
from bugs.forms import BugForm, BugInputForm

def index(request):
    l = Bug.all().fetch(1000)
    return HttpResponse(str( l ))

# Login required for request.user
@login_required
def new(request):
    # We cannot use the generic view here, if we want to override the user
    # field with the current user.

    if request.method == 'POST':
        # `Add' current user to request.POST, which then is used to initialize
        # the form.
        request.POST = request.POST.copy() # make request.POST mutable.
        request.POST.update({ 'user': request.user.key() })

        # We use the BugForm here because it accepts the user field
        form = BugForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('bugs.views.index'))
        
        form = BugInputForm(request.POST)
        # This way, we remove the user and the ctime field when validation
        # fails.
    else:
        # Initialize a form without the user and ctime fields.
        form = BugInputForm()
    return render_to_response('bugs/new.html', { 'form': form, }, RequestContext(request))
