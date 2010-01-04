# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import Template
from django.template.loader import render_to_string, get_template
from django.utils.translation import ugettext_lazy as _

from rpx.templatetags.rpx_tags import rpx_link

LOGOUT_URL = getattr(settings, 'LOGOUT_URL')
login_template_loc = 'rpx/rpx_link.html'

def login_logout(request, login_text = _('login'), logout_text = _('logout')):
    login_next = request.GET['next'] if request.GET.has_key('next') else request.path
    logout_next = request.GET['next'] if request.GET.has_key('next') else request.path
    logout_template = Template(
        '<a href="%(logout_url)s%(next)s">%(logout)s</a></span>' %
        { 'logout_url': LOGOUT_URL,
          'next': '?next=' + logout_next if logout_next else '',
          'logout': logout_text, }
    )
    return {
        'login_link': render_to_string(login_template_loc, rpx_link(None, login_text, login_next)),
        'logout_link': logout_template.render(None),
    }
