#encoding: utf-8
from django.conf import settings

PRODUCT_MODEL = getattr(settings, 'PLUGSHOP_PRODUCT_MODEL', 
                        'plugshop.models.product.Product')

GROUP_MODEL = getattr(settings, 'PLUGSHOP_GROUP_MODEL', 
                        'plugshop.models.group.Group')
                        
OPTION_MODEL = getattr(settings, 'PLUGSHOP_OPTION_MODEL', 
                        'plugshop.models.option.Option')

PRODUCT_GROUPS_MODEL = getattr(settings, 'PLUGSHOP_PRODUCT_GROUPS_MODEL', 
                            'plugshop.models.product_groups.ProductGroups')
                        
PRODUCT_OPTIONS_MODEL = getattr(settings, 'PLUGSHOP_PRODUCT_OPTIONS_MODEL', 
                            'plugshop.models.product_options.ProductOptions')

SHIPPING_TYPE_MODEL = getattr(settings, 'PLUGSHOP_SHIPPING_TYPE_MODEL', 
                            'plugshop.models.shipping.ShippingType')
                                
SHIPPING_ADDRESS_MODEL = getattr(settings, 'PLUGSHOP_SHIPPING_ADDRESS_MODEL', 
                            'plugshop.models.shipping.ShippingAddress')

ORDER_MODEL = getattr(settings, 'PLUGHOSP_ORDER_MODEL', 
                    'plugshop.models.order.Order')
ORDER_PRODUCTS_MODEL = getattr(settings, 'PLUGHOSP_ORDER_PRODUCTS_MODEL', 
                    'plugshop.models.order_products.OrderProducts')
