from django.utils.translation import ugettext as _

from django.db import models

from plugshop import settings

from plugshop.utils import load_class

from plugshop.models.product import *
from plugshop.models.group import *
from plugshop.models.option import *
from plugshop.models.product_options import *
from plugshop.models.shipping import *
from plugshop.models.order import *
from plugshop.models.order_products import *

models.ManyToManyField(load_class(settings.OPTION_MODEL),  
                        through=load_class(settings.PRODUCT_OPTIONS_MODEL),
                        related_name="product_options",
                        verbose_name=_('Product options')
                    ).contribute_to_class(ProductAbstract, 'options')

models.ManyToManyField(load_class(settings.PRODUCT_MODEL),
                        through=load_class(settings.ORDER_PRODUCTS_MODEL),
                        related_name="order_products",
                        verbose_name=_('Order products')
                    ).contribute_to_class(OrderAbstract, 'products')

__all__ = [
    'ProductAbstract',
    'Product',
    
    'Group',
    'GroupAbstract',
    
    'Option', 
    'ProductOptions', 
    'ShippingType',
    'ShippingAddress',
    'Order',
    'OrderProducts',
]