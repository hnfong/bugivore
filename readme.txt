== Introduction ==

This is the alpha release of the Django-RPX-GAE-GAE authentication backend 0.1. 

It is in alpha stage since it has only been tested with app-engine-patch-sample-1.0 
that uses Django 1.0.2 and the mileage of this is limited.

== Known issues/drawbacks that will be fixed ==

No timeout on request to RPX server.

No code review has been done.

There are a few todo in the code that needs to be resolved.

For some reasons, I have had a few problems with the deployment, causing internal 
server errors at the app enging. Currently investigating, and hopefully the demo 
site running this version will be stable in the future 
(http://bergsell.appspot.com/rpx_demo/).

Anyway, I think that you should be able to use this in prototype applications. 
Feedback is needed to be able to take this to a stable and secure backend.

== Installation instructions ==

1. Unpack the rpx module in your project.

2. Add 'rpx' in the INSTALLED_APPS variable in your settings.

3. Add rpx as an authentication backend:

AUTHENTICATION_BACKENDS = ('rpx.backends.RpxBackend',
                           'django.contrib.auth.backends.ModelBackend')

4. Add rpx_tags in your global tags to enable easy access to rpx tags

GLOBALTAGS = (
    'rpx.templatetags.rpx_tags',
)

5. Configure the settings in the settings.py in the rpx module. You need to set 
the RPXNOW_API_KEY, RPXNOW_REALM, and configure the list of trusted providers.

Now it should be possible to use the rpx backend. In your templates you should 
be able to add the tag {% rpx_iframe next %} where the next param is the url
to where you would like to redirect the user after a successful authentication. 

The example below will send the user to /main/ from the login page upon successful
authinticaiton.

return render_to_response(request, 'login.html',
                              {'next': '/main/', })

Feedback is highly appreciated.
