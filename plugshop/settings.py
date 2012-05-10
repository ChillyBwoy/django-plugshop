#encoding: utf-8
from django.utils.translation import ugettext as _
from django.conf import settings

REQUEST_NAMESPACE = getattr(settings, 'PLUGSHOP_REQUEST_NAMESPACE', 'cart')
SESSION_NAMESPACE = getattr(settings, 'PLUGSHOP_SESSION_NAMESPACE', 'cart')

PRODUCT_MODEL = getattr(settings, 'PLUGSHOP_PRODUCT_MODEL', 
                        'plugshop.models.product.Product')

GROUP_MODEL = getattr(settings, 'PLUGSHOP_GROUP_MODEL', 
                        'plugshop.models.group.Group')
                        
OPTION_MODEL = getattr(settings, 'PLUGSHOP_OPTION_MODEL', 
                        'plugshop.models.option.Option')
                        
PRODUCT_OPTIONS_MODEL = getattr(settings, 'PLUGSHOP_PRODUCT_OPTIONS_MODEL', 
                            'plugshop.models.product_options.ProductOptions')

SHIPPING_TYPE_MODEL = getattr(settings, 'PLUGSHOP_SHIPPING_TYPE_MODEL', 
                            'plugshop.models.shipping.ShippingType')
                                
SHIPPING_MODEL = getattr(settings, 'PLUGSHOP_SHIPPING_MODEL', 
                            'plugshop.models.shipping.Shipping')

ORDER_MODEL = getattr(settings, 'PLUGHOSP_ORDER_MODEL', 
                    'plugshop.models.order.Order')
                    
ORDER_PRODUCTS_MODEL = getattr(settings, 'PLUGHOSP_ORDER_PRODUCTS_MODEL', 
                    'plugshop.models.order_products.OrderProducts')



STATUS_CHOICES = getattr(settings, 'PLUGHOSP_STATUS_CHOICES', (
                            (1, _('Created')),
                            (2, _('Confirmed')),
                            (3, _('Denied')),
                            (4, _('Delivered')),
                        ))

STATUS_CHOICES_START = getattr(settings, 'PLUGHOSP_STATUS_CHOICES_START', 
                                STATUS_CHOICES[0])
STATUS_CHOICES_FINISH = getattr(settings, 'PLUGHOSP_STATUS_CHOICES_FINISH',
                                STATUS_CHOICES[-1])