# -*- coding: utf-8 -*-
import re

def remove_body_background(template):
    lines = []
    pattern = re.compile(r'.* body.*background.*')
    for l in template.split("\n"):
        if not pattern.match(l):
            lines.append(l)
    return "\n".join(lines)

def _patch_debug():
    import inspect
    import logging

    from django.views import debug
    debug.TECHNICAL_404_TEMPLATE = remove_body_background(debug.TECHNICAL_404_TEMPLATE)
    logging.debug('%s: patched debug view 404' % inspect.getfile(inspect.currentframe()))

_patch_debug()
