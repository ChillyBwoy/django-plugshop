#encoding: utf-8
from django.utils.translation import ugettext as _
from django.conf import settings

REQUEST_NAMESPACE = getattr(settings, 'PLUGSHOP_REQUEST_NAMESPACE', 'cart')
SESSION_NAMESPACE = getattr(settings, 'PLUGSHOP_SESSION_NAMESPACE', 'cart')

PRODUCT_MODEL_DEFAULT = 'plugshop.models.product.Product'
PRODUCT_MODEL = getattr(settings, 'PLUGSHOP_PRODUCT_MODEL', 
                            PRODUCT_MODEL_DEFAULT)

CATEGORY_MODEL_DEFAULT = 'plugshop.models.category.Category'
CATEGORY_MODEL = getattr(settings, 'PLUGSHOP_CATEGORY_MODEL', 
                            CATEGORY_MODEL_DEFAULT)

SHIPPING_MODEL_DEFAULT =  'plugshop.models.shipping.Shipping'
SHIPPING_MODEL = getattr(settings, 'PLUGSHOP_SHIPPING_MODEL', 
                            SHIPPING_MODEL_DEFAULT)

SHIPPING_TYPE_MODEL_DEFAULT = 'plugshop.models.shipping_type.ShippingType'
SHIPPING_TYPE_MODEL = getattr(settings, 'PLUGSHOP_SHIPPING_TYPE_MODEL', 
                                SHIPPING_TYPE_MODEL_DEFAULT)

ORDER_MODEL_DEFAULT = 'plugshop.models.order.Order'
ORDER_MODEL = getattr(settings, 'PLUGHOSP_ORDER_MODEL', ORDER_MODEL_DEFAULT)
                
ORDER_PRODUCTS_MODEL_DEFAULT = 'plugshop.models.order_products.OrderProducts'
ORDER_PRODUCTS_MODEL = getattr(settings, 'PLUGHOSP_ORDER_PRODUCTS_MODEL', 
                                    ORDER_PRODUCTS_MODEL_DEFAULT)


STATUS_CHOICES = getattr(settings, 'PLUGHOSP_STATUS_CHOICES', (
                            (1, _('Created')),
                            (2, _('Confirmed')),
                            (3, _('Denied')),
                            (4, _('Delivered')),
                        ))

STATUS_CHOICES_START = getattr(settings, 'PLUGHOSP_STATUS_CHOICES_START', 
                                STATUS_CHOICES[0][0])
STATUS_CHOICES_FINISH = getattr(settings, 'PLUGHOSP_STATUS_CHOICES_FINISH',
                                STATUS_CHOICES[-1][0])
