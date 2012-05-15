from plugshop import settings
from django.core import exceptions
from django.utils.importlib import import_module
from django.db.models import get_model
from django.core.cache import cache

def load_class(path):
    module_path, class_name = path.rsplit('.', 1)
    
    print module_path, class_name
    print '==================================='
    
    module = import_module(module_path)
    cl = getattr(module, class_name)
    return cl

def is_default_model(name):
    model = getattr(settings, "%s_MODEL" % name, None)
    default_model = getattr(settings, "%s_MODEL_DEFAULT" % name, None)

    if model is not None and default_model is not None:
        return model == default_model
    else:
        return False

def serialize_model(instance):
    data = {}
    for field in instance._meta.fields:
        data[field.name] = field.value_to_string(instance)
    return data


def get_categories(*args, **kwargs):
    categories = cache.get('plugshop_categories')
    if categories is None:
        categories = load_class(settings.CATEGORY_MODEL).objects.all()
        cache.set('plugshop_categories', categories)
    return categories
