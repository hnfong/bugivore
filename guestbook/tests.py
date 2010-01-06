# -*- coding: utf-8 -*-

from django.test.client import Client

from guestbook import views

# TODO: The following tests do not work, fix them
__test__ = {
"Test guestbook should give 200 and render guestbook.views.list": """
>>> c = Client()
>>> response = c.get('/guestbook/')
>>> response.status_code
200
>>> response.content == views.list
''
""",
"Test guestbook/sign should be protected": """
>>> c = Client()
>>> response = c.get('/guestbook/sign/')
>>> response.status_code
302
>>> response.content
''
""",
}
