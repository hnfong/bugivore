# -*- coding: utf-8 -*-
# Partly taken from app-engine-patch/myapp/models.py
#   http://code.google.com/p/app-engine-patch/ (in the toy application myapp/)
from django.db.models import signals
from google.appengine.ext import db
from ragendja.dbutils import cleanup_relations
from datetime import datetime
from random import random, getrandbits
from string import letters, digits

def auto_cleanup_relations(model):
    """
    auto_cleanup_relations(model) signals model to clean up dangling
    references when an instance of model is deleted from the database.
    """
    signals.pre_delete.connect(cleanup_relations, sender=model)

def auto_delete_parent(model):
    """
    auto_delete_parent(model) signals model to delete parent when an instance
    of model is deleted from the datastore.
    """
    signals.pre_delete.connect(delete_parent, sender=model)

def delete_parent(instance, **kargs):
    db.delete(instance.parent_key())

def random_key():
    """
    Generate a random key, suitable for use as key_name, based on current time
    and a random number.
    """
    return datetime.utcnow().strftime('%Y%m%d%H%M%S') + str(getrandbits(64))
