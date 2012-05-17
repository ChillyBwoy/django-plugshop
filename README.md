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

        PLUGSHOP_PRODUCT_MODEL = 'testshop.myshop.models.Product'  
        PLUGSHOP_CATEGORY_MODEL = 'testshop.myshop.models.Category'
    
* Run `python manage.py syncdb`


Configuration
=============

Models:

* `PLUGSHOP_PRODUCT_MODEL`
* `PLUGSHOP_CATEGORY_MODEL`
* `PLUGSHOP_SHIPPING_MODEL`
* `PLUGSHOP_SHIPPING_TYPE_MODEL`
* `PLUGSHOP_ORDER_MODEL`
* `PLUGSHOP_ORDER_PRODUCTS_MODEL`

Possible values of the status of the order are stored in `PLUGSHOP_STATUS_CHOICES` tuple. Default values are:
    
    PLUGSHOP_STATUS_CHOICES = (
        (1, _('Created')),
        (2, _('Confirmed')),
        (3, _('Denied')),
        (4, _('Delivered')),
    )
    
Cart
====

        #views.py
        def my_view(request):
            cart = request.cart
    
Or
    
        #settings.py
        PLUGSHOP_REQUEST_NAMESPACE = 'my_cart_namespace'
        
        #views.py
        def my_view(request):
            cart = request.my_cart_namespace
