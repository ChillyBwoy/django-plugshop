from plugshop import settings
from django.core import exceptions
from django.utils.importlib import import_module
from django.db.models import get_model


def load_class(path):
    module_path, class_name = path.rsplit('.', 1)
    module = import_module(module_path)
    
    print module_path, class_name
    print '==================================='
    
    cl = getattr(module, class_name)
    return cl
    
def serialize_model(instance):
    data = {}
    for field in instance._meta.fields:
        data[field.name] = field.value_to_string(instance)
    return data