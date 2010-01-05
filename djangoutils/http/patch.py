# -*- coding: utf-8 -*-
import re

def _remove_body_background(template):
    lines = []
    pattern = re.compile(r'.* body.*background.*')
    for l in template.split("\n"):
        if not pattern.match(l):
            lines.append(l)
    return "\n".join(lines)

def patch_debug():
    from django.views import debug
    debug.TECHNICAL_404_TEMPLATE = _remove_body_background(debug.TECHNICAL_404_TEMPLATE)
