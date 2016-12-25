Django Plugshop
===============

A set of useless abstract models

Requirements
============

1. [django](https://github.com/django/django/) >= 1.4, <=1.5
2. [django-mptt](https://github.com/django-mptt/django-mptt/)

Installation
============

* Add the `plugshop` directory to your Python path.

* Add `plugshop` to your `INSTALLED_APPS`

* Add the following middleware to your project's settings.py file:

        `plugshop.middleware.CartMiddleware`

* Add the request context processor:

        TEMPLATE_CONTEXT_PROCESSORS = (
            # ...
            'django.core.context_processors.request',
            # ...
        )

* Add URL-patterns:

        urlpatterns = patterns('',  
            url(r'^shop/', include('plugshop.urls')),  
        )

* Override default models. Example:

        PLUGSHOP_MODELS = {
            'PRODUCT': 'myshop.Product',
            'CATEGORY': 'myshop.Category',
            'ORDER': 'myshop.Order',
        }

* Run `python manage.py syncdb`

* Profit!

Configuration
=============

Models:

        PLUGSHOP_MODELS = {
            'PRODUCT': 'plugshop.Product',
            'CATEGORY': 'plugshop.Category',
            'ORDER': 'plugshop.Order',
            'ORDER_PRODUCTS': 'plugshop.OrderProducts',
        }

Forms:

        PLUGSHOP_FORMS = {
            'ORDER': 'plugshop.forms.OrderForm',
        }

Config:

        PLUGSHOP_CONFIG = {
            'REQUEST_NAMESPACE': 'cart',
            'SESSION_NAMESPACE': 'cart',
            'URL_PREFIX': 'shop/',
        }

Other options:

        PLUGSHOP_OPTIONS = {
            # Possible values of the status of the order. Default values:
            'STATUS_CHOICES': (
                (1, _('Created')),
                (2, _('Confirmed')),
                (3, _('Denied')),
                (4, _('Shipped')),
                (5, _('Completed')),
            ),
        }

Cart
====

        #views.py
        def my_view(request):
            cart = request.cart

Or

        #settings.py
        PLUGSHOP_CONFIG = {
            ...
            'REQUEST_NAMESPACE': 'my_cart_namespace',
            ...
        }

        #views.py
        def my_view(request):
            cart = request.my_cart_namespace
