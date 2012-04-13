from django.utils.importlib import import_module

def load_class(path):
    module_path, class_name = path.rsplit('.', 1)
    module = import_module(module_path)

    cl = getattr(module, class_name)
    return cl
