# -*- coding: utf-8 -*-

# The following function is taken from stack overflow
#   http://stackoverflow.com/questions/250357/smart-truncate-in-python
import textwrap
def truncate(text, max_size):
    if len(text) <= max_size:
        return text
    return textwrap.wrap(text, max_size-3)[0] + "..."
