from django.utils.translation import ugettext as _

from django.db import models

from plugshop import settings

from plugshop.utils import load_class

from plugshop.models.product import *
from plugshop.models.category import *
from plugshop.models.option import *
from plugshop.models.product_options import *
from plugshop.models.shipping import *
from plugshop.models.order import *
from plugshop.models.order_products import *

models.ManyToManyField(load_class(settings.OPTION_MODEL),  
                        through=load_class(settings.PRODUCT_OPTIONS_MODEL),
                        related_name="products",
                        verbose_name=_('option list')
                    ).contribute_to_class(load_class(settings.PRODUCT_MODEL), 'options')

models.ForeignKey(load_class(settings.CATEGORY_MODEL),
                        verbose_name=_('category'),
                        related_name='products',
                        blank=True,
                        null=True
                    ).contribute_to_class(load_class(settings.PRODUCT_MODEL), 'category')

models.ManyToManyField(load_class(settings.PRODUCT_MODEL),
                        through=load_class(settings.ORDER_PRODUCTS_MODEL),
                        related_name="products",
                        verbose_name=_('products')
                    ).contribute_to_class(load_class(settings.ORDER_MODEL), 'products')

__all__ = [
    'ProductAbstract',
    'Product',
    
    'Category',
    'CategoryAbstract',

    'Option', 
    'ProductOptions', 

    'ShippingType',
    'Shipping',

    'Order',
    'OrderProducts',
]