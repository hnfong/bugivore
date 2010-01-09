# -*- coding: utf-8 -*-

# The following function is taken from Stack Overflow
#   http://stackoverflow.com/questions/250357/smart-truncate-in-python
import textwrap
def truncate(text, max_size):
    if len(text) <= max_size:
        return text
    return textwrap.wrap(text, max_size-3)[0] + "..."

# The following function is taken from Stack Overflow
#   http://stackoverflow.com/questions/699468/python-html-sanitizer-scrubber-filter/812865#812865
from BeautifulSoup import BeautifulSoup, NavigableString

acceptable_elements = ['a', 'abbr', 'acronym', 'address', 'area', 'b', 'big',
      'blockquote', 'br', 'button', 'caption', 'center', 'cite', 'code', 'col',
      'colgroup', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt', 'em',
      'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 
      'ins', 'kbd', 'label', 'legend', 'li', 'map', 'menu', 'ol', 
      'p', 'pre', 'q', 's', 'samp', 'small', 'span', 'strike',
      'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
      'thead', 'tr', 'tt', 'u', 'ul', 'var']

acceptable_attributes = ['abbr', 'accept', 'accept-charset', 'accesskey',
  'action', 'align', 'alt', 'axis', 'border', 'cellpadding', 'cellspacing',
  'char', 'charoff', 'charset', 'checked', 'cite', 'clear', 'cols',
  'colspan', 'color', 'compact', 'coords', 'datetime', 'dir', 
  'enctype', 'for', 'headers', 'height', 'href', 'hreflang', 'hspace',
  'id', 'ismap', 'label', 'lang', 'longdesc', 'maxlength', 'method',
  'multiple', 'name', 'nohref', 'noshade', 'nowrap', 'prompt', 
  'rel', 'rev', 'rows', 'rowspan', 'rules', 'scope', 'shape', 'size',
  'span', 'src', 'start', 'summary', 'tabindex', 'target', 'title', 'type',
  'usemap', 'valign', 'value', 'vspace', 'width']

def clean_html( fragment, acceptable_elements=acceptable_elements, acceptable_attributes=acceptable_attributes ):
    soup = BeautifulSoup( fragment.strip() )
    def cleanup( soup ):
        for tag in soup:
            if not isinstance( tag, NavigableString):
                if tag.name not in acceptable_elements:
                    tag.extract()
                else:
                    for attr in tag._getAttrMap().keys():
                        if attr not in acceptable_attributes:
                            del tag[attr]
                    cleanup( tag )
    cleanup( soup )
    return unicode( soup )
