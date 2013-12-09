# -*- coding: utf-8 -*-

from django.core import exceptions
from django.core.cache import cache
from django.db.models import get_model
from django.db.models.loading import get_model as django_get_model
from django.utils.importlib import import_module

from plugshop import settings


def get_model(path):
    model = django_get_model(*path.split('.'))
    return model


def load_class(path):
    module_path, class_name = path.rsplit('.', 1)
    module = import_module(module_path)
    cl = getattr(module, class_name)
    return cl


def is_default_model(name):
    model = getattr(settings, "%s_MODEL" % name.upper(), None)
    default_model = getattr(settings, "%s_MODEL_DEFAULT" % name.upper(), None)
    
    if model is not None and default_model is not None:
        return model == default_model
    else:
        return False


def serialize_model(instance):
    data = {}
    for field in instance._meta.fields:
        data[field.name] = field.value_to_string(instance)
    return data


def serialize_queryset(queryset):
    return [serialize_model(item) for item in queryset]