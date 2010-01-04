# -*- coding: utf-8 -*-
# Partly taken from app-engine-patch/myapp/models.py
#   http://code.google.com/p/app-engine-patch/
from django.db.models import signals
from google.appengine.ext import db
from ragendja.dbutils import cleanup_relations

def auto_cleanup_relations(model):
    signals.pre_delete.connect(cleanup_relations, sender=model)
