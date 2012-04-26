from django.utils.translation import ugettext as _

from django.db import models

from plugshop import settings

from plugshop.utils import load_class

from plugshop.models.product import *
from plugshop.models.group import *
from plugshop.models.option import *
from plugshop.models.product_options import *
from plugshop.models.product_groups import *

                    
models.ManyToManyField(load_class(settings.GROUP_MODEL),
                        through=load_class(settings.PRODUCT_GROUPS_MODEL),
                        related_name="product_groups",
                        verbose_name=_('Product groups')
                    ).contribute_to_class(ProductAbstract, 'groups')

models.ManyToManyField(load_class(settings.OPTION_MODEL),  
                        through=load_class(settings.PRODUCT_OPTIONS_MODEL),
                        related_name="product_options",
                        verbose_name=_('Product options')
                    ).contribute_to_class(ProductAbstract, 'options')
__all__ = [
    'Product',
    'Group',
    'Option', 
    'ProductGroups',
    'ProductOptions', 
]