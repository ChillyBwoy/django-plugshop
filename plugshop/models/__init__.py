from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User

from plugshop import settings
from plugshop.utils import load_class, get_categories

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# from plugshop.models.product import *
# from plugshop.models.category import *
# from plugshop.models.option import *
# from plugshop.models.product_options import *
# from plugshop.models.shipping import *
# from plugshop.models.shipping_type import *
# from plugshop.models.order import *
# from plugshop.models.order_products import *

# __all__ = [
#     'ProductAbstract',
#     'CategoryAbstract',
#     'ProductOptionsAbstract', 
#     'OptionAbstract',
#     'ShippingAbstract',
#     'ShippingTypeAbstract',
#     'OrderAbstract',
#     'OrderProductsAbstract'
# ]
# 
# def import_default(name, settings, where=[]):
#     default_name = "%s_DEFAULT" % name
#     model = getattr(settings, name)
#     default_model = getattr(settings, default_name)
# 
#     if model == default_model:
#         cls = load_class(model)
#         #setattr(cls._meta, 'app_label', 'plugshop')
#         where.append(default_model.split('.')[-1])
# 
# for m in ['CATEGORY_MODEL',
#             'PRODUCT_MODEL', 
#             'OPTION_MODEL',
#             'PRODUCT_OPTIONS_MODEL',
#             'SHIPPING_TYPE_MODEL',
#             'SHIPPING_MODEL',
#             'ORDER_MODEL',
#             'ORDER_PRODUCTS_MODEL']:
#     import_default(m, settings, __all__)

PRODUCT_CLASS = load_class(settings.PRODUCT_MODEL)
OPTION_CLASS = load_class(settings.OPTION_MODEL)
PRODUCT_OPTIONS_CLASS = load_class(settings.PRODUCT_OPTIONS_MODEL)
CATEGORY_CLASS = load_class(settings.CATEGORY_MODEL)
ORDER_CLASS = load_class(settings.ORDER_MODEL)
ORDER_PRODUCTS_CLASS = load_class(settings.ORDER_PRODUCTS_MODEL)
SHIPPING_TYPE_CLASS = load_class(settings.SHIPPING_TYPE_MODEL)
SHIPPING_CLASS = load_class(settings.SHIPPING_MODEL)

models.ManyToManyField(OPTION_CLASS, 
                        through=PRODUCT_OPTIONS_CLASS,
                        related_name="products",
                        verbose_name=_('option list')
                    ).contribute_to_class(PRODUCT_CLASS, 'options')

models.ForeignKey(CATEGORY_CLASS,
                        verbose_name=_('category'),
                        related_name='products',
                        blank=True,
                        null=True
                    ).contribute_to_class(PRODUCT_CLASS, 'category')

models.ManyToManyField(PRODUCT_CLASS,
                        through=ORDER_PRODUCTS_CLASS,
                        related_name="products",
                        verbose_name=_('products')
                    ).contribute_to_class(ORDER_CLASS, 'products')

models.ForeignKey(User, 
                    verbose_name=_('user')
                ).contribute_to_class(ORDER_CLASS, 'user')
                            
models.ForeignKey(ORDER_CLASS,
                    verbose_name=_('order')
                ).contribute_to_class(ORDER_PRODUCTS_CLASS, 'order')

models.ForeignKey(PRODUCT_CLASS,
                    verbose_name=_('product')
                ).contribute_to_class(ORDER_PRODUCTS_CLASS, 'product')

models.ForeignKey(PRODUCT_CLASS,
                    verbose_name=_('product')
                ).contribute_to_class(PRODUCT_OPTIONS_CLASS, 'product')

models.ForeignKey(OPTION_CLASS,
                    verbose_name=_('option')
                ).contribute_to_class(PRODUCT_OPTIONS_CLASS, 'option')


models.ForeignKey(SHIPPING_TYPE_CLASS,
                    verbose_name=_('shipping type'), 
                    blank=True, 
                    null=True
                ).contribute_to_class(SHIPPING_CLASS, 'type')

# models.OneToOneField(ORDER_CLASS,
#                     verbose_name=_('order'), 
#                     primary_key=True
#                 ).contribute_to_class(SHIPPING_CLASS, 'order')

@receiver(post_save, sender=SHIPPING_CLASS)
def remove_null_shipping(sender, instance, created, **kwargs):
    if instance.type is None:
        instance.delete()

@receiver(pre_save, sender=ORDER_CLASS)
def set_delivered(sender, instance, **kwargs):
    if instance.status == settings.STATUS_CHOICES_FINISH:
        instance.delivered_at = datetime.datetime.now()
    else:
        instance.delivered_at = None

post_save.connect(get_categories, sender=CATEGORY_CLASS)