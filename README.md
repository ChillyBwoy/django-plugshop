Django Plugshop
===============

A set of useless abstract models

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
            'PRODUCT': 'testshop.myshop.models.Product',
            'CATEGORY': 'testshop.myshop.models.Category',
        }
    
* Run `python manage.py syncdb`


Configuration
=============

Models:

        PLUGSHOP_MODELS = {
            'PRODUCT': 'plugshop.models.product.Product',
            'CATEGORY': 'plugshop.models.category.Category',
            'ORDER': 'plugshop.models.order.Order',
            'ORDER_PRODUCTS': 'plugshop.models.order_products.OrderProducts',
        }

Config:
    
    
        PLUGSHOP_CONFIG = {
            'REQUEST_NAMESPACE': 'cart',
            'SESSION_NAMESPACE': 'cart',
        }

Other options:

        PLUGSHOP_OPTIONS = {
            # Possible values of the status of the order. Default values:
            'STATUS_CHOICES': (
                (1, _('Created')),
                (2, _('Confirmed')),
                (3, _('Denied')),
                (4, _('Delivered')),
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
