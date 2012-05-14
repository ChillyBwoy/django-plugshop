Django Plugshop
===============

A set of useless abstract models

Installation
============

* Add the `plugshop` directory to your Python path.

* Add `plugshop` to your 'INSTALLED_APPS'

* Add the following middleware to your project's settings.py file:

        `plugshop.middleware.CartMiddleware`

* Override default models:

        PLUGSHOP_PRODUCT_MODEL = 'testshop.myshop.models.Product'
        PLUGSHOP_CATEGORY_MODEL = 'testshop.myshop.models.Category'
    
* Run `python manage.py syncdb`