#encoding: utf-8
from django.conf import settings

# PRODUCT_MODEL = getattr(settings, 'PLUGSHOP_PRODUCT_MODEL', 
#                         'plugshop.models.defaults.Product')
# GROUP_MODEL = getattr(settings, 'PLUGSHOP_GROUP_MODEL', 
#                         'plugshop.models.defaults.ProductGroup')

PRODUCT_MODEL = getattr(settings, 'PLUGSHOP_PRODUCT_MODEL', 
                        'plugshop.models.product.Product')

GROUP_MODEL = getattr(settings, 'PLUGSHOP_GROUP_MODEL', 
                        'plugshop.models.group.Group')
                        
PRODUCT_GROUPS_MODEL = getattr(settings, 'PLUGSHOP_PRODUCT_GROUPS_MODEL', 
                                'plugshop.models.product_groups.ProductGroups')
                        
PRODUCT_OPTIONS_MODEL = getattr(settings, 'PLUGSHOP_PRODUCT_OPTIONS_MODEL', 
                                'plugshop.models.product_options.ProductOptions')
                        
OPTION_MODEL = getattr(settings, 'PLUGSHOP_OPTION_MODEL', 
                        'plugshop.models.option.Option')
