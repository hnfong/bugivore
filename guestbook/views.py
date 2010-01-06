# -*- coding: utf-8 -*-
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from djangoutils.auth.decorators import login_required

from guestbook.models import Greeting

def add_message(request):
    request.login_message = _('You need to login to sign our guestbook.')
    return request

def list(request, context=None):
    greetings = Greeting.all().order('-date').fetch(10)
    return render_to_response('guestbook/list.html', { 'greetings': greetings }, RequestContext(request))

@login_required(request_processor = add_message)
def sign(request, context=None):
    error = []
    # set the default logout location to the frontpage of guestbook
    request.GET = request.GET.copy() # make GET mutable
    request.GET[REDIRECT_FIELD_NAME] = reverse('guestbook.views.list')
    if request.method == 'POST':

        message = request.POST.get('message')

        if message and message.strip():
            message = message.strip()
            greeting = Greeting(author = request.user, content = message)
            greeting.save()
            return list(request)
        else:
            error.append('Message cannot be empty.')
    return render_to_response('guestbook/sign.html', { 'error': error }, RequestContext(request))
