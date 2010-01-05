# -*- coding: utf-8 -*-
# Partly taken from app-engine-patch/myapp/models.py
#   http://code.google.com/p/app-engine-patch/ (in the toy application myapp/)
from django.db.models import signals
from google.appengine.ext import db
from ragendja.dbutils import cleanup_relations

def auto_cleanup_relations(model):
    """
    auto_cleanup_relations(model) signals model to clean up dangling
    references when an instance of model is deleted from the database.
    """
    signals.pre_delete.connect(cleanup_relations, sender=model)
