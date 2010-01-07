# -*- coding: utf-8 -*-
# Patch over app-engine-patch (see (django-1.1.zip)/django/forms.model.py)
from django.utils.translation import ugettext_lazy as _

# The following function takes codes from app-engine-patch
# See also the code in unpatched django:
#   http://code.djangoproject.com/browser/django/trunk/django/forms/models.py
#
# This function recovers the (slightly modified) construct_instance API from
# the original django-source, which is removed from app-engine-patch.
def construct_instance(form, model, instance, fields=None, exclude=None,
        fail_message=_('constructed'), initialize={}):
    """
    Constructs and returns a model instance from the bound ``form``'s
    ``cleaned_data``, but does not save the returned instance to the
    database.
    """
    from google.appengine.ext import db
    opts = model._meta

    cleaned_data = form.cleaned_data
    # Since GAE models validate at construction time we have to collect
    # all data before setting it
    converted_data = initialize.copy()
    # Simulate a property for key_name
    for f in opts.fields + (db.StringProperty(name='key_name'),):
        if not f.editable \
                or not f.name in cleaned_data:
            continue
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        if f.name in cleaned_data:
            value = cleaned_data[f.name]
            converted_data[f.name] = f.make_value_from_form(value)
    local_field_names = [f.name for f in opts.fields]

    # Create the instance (if necessary) and then set all values
    try:
        if instance is None:
            instance = model(**converted_data)
        else:
            for name, value in converted_data.items():
                if name in local_field_names:
                    setattr(instance, name, value)
    except db.BadValueError, err:
        raise ValueError(_('The %s could not be %s (%s)') %
                         (opts.object_name, fail_message, err))

    return instance

# The following code refactor the save_instance method in app-engine-patch
# with the above construct_instance API.
def save_instance(form, model, instance, fields=None, fail_message=_('saved'),
                  commit=True, exclude=None, construct=True, initialize={}):
    """
    Saves bound Form ``form``'s cleaned_data into model instance
    ``instance``.
    
    If commit=True, then the changes to ``instance`` will be saved to
    the
    database. Returns ``instance``.
    
    If construct=False, assume ``instance`` has already been
    constructed and
    just needs to be saved.
    """
    # We first check for validation errors, because there is no point in
    # constructing an instance from invalid data.
    opts = model._meta
    if form.errors:
        raise ValueError(_("The %s could not be %s because the data didn't"
                         " validate.") % (opts.object_name, fail_message))
    if construct:
        instance = construct_instance(form, model, instance, fields, exclude, fail_message, initialize)

    if commit:
        # If we are committing, save the instance immediately.
        instance.put()
    else:
        form.save_m2m = lambda: None

    return instance
