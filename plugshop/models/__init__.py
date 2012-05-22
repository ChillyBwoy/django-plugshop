import datetime
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User

from plugshop import settings
from plugshop.utils import load_class, get_categories

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from plugshop.models.product import *
from plugshop.models.category import *
from plugshop.models.shipping import *
from plugshop.models.shipping_type import *
from plugshop.models.order import *
from plugshop.models.order_products import *
from mptt.fields import TreeForeignKey

PRODUCT_CLASS = load_class(settings.PRODUCT_MODEL)
CATEGORY_CLASS = load_class(settings.CATEGORY_MODEL)
ORDER_CLASS = load_class(settings.ORDER_MODEL)
ORDER_PRODUCTS_CLASS = load_class(settings.ORDER_PRODUCTS_MODEL)
SHIPPING_TYPE_CLASS = load_class(settings.SHIPPING_TYPE_MODEL)
SHIPPING_CLASS = load_class(settings.SHIPPING_MODEL)

PRODUCT_CLASS.add_to_class('category', TreeForeignKey(CATEGORY_CLASS,
                                        verbose_name=_('category'),
                                        related_name='products',
                                        blank=True,
                                        null=True))

ORDER_CLASS.add_to_class('products', models.ManyToManyField(PRODUCT_CLASS,
                                        through=ORDER_PRODUCTS_CLASS,
                                        related_name="products",
                                        verbose_name=_('products')))

ORDER_CLASS.add_to_class('user', models.ForeignKey(User,
                                        verbose_name=_('user')))

ORDER_PRODUCTS_CLASS.add_to_class('order', models.ForeignKey(ORDER_CLASS,
                                        verbose_name=_('order')))

ORDER_PRODUCTS_CLASS.add_to_class('product', models.ForeignKey(PRODUCT_CLASS, 
                                        verbose_name=_('product')))

SHIPPING_CLASS.add_to_class('type', models.ForeignKey(SHIPPING_TYPE_CLASS,
                                        verbose_name=_('shipping type')))

SHIPPING_CLASS.add_to_class('order', models.OneToOneField(ORDER_CLASS,
                                        verbose_name=_('order')))

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

@receiver(pre_save, sender=ORDER_CLASS)
def set_updated(sender, instance, **kwargs):
    instance.updated_at = datetime.datetime.now()

@receiver(pre_save, sender=ORDER_CLASS)
def generate_number(sender, instance, **kwargs):
    if instance.id is None:
        today = datetime.datetime.now()
        today_orders = ORDER_CLASS.objects.filter(
                            created_at__year=today.year,
                            created_at__month=today.month,
                            created_at__day=today.day
                        )
        num = int("%s%s" % (today.strftime("%y%m%d"), len(today_orders) + 1))
        instance.number = num

post_save.connect(get_categories, sender=CATEGORY_CLASS)