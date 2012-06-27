import datetime
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

from plugshop import settings
from plugshop.utils import load_class, get_categories

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from plugshop.models.product import *
from plugshop.models.category import *
from plugshop.models.order import *
from plugshop.models.order_products import *
from mptt.fields import TreeForeignKey

PRODUCT_CLASS = load_class(settings.PRODUCT_MODEL)
CATEGORY_CLASS = load_class(settings.CATEGORY_MODEL)
ORDER_CLASS = load_class(settings.ORDER_MODEL)
ORDER_PRODUCTS_CLASS = load_class(settings.ORDER_PRODUCTS_MODEL)

PRODUCT_CLASS.add_to_class('category', TreeForeignKey(CATEGORY_CLASS,
                                        verbose_name=_('category'),
                                        related_name='products',
                                        blank=True,
                                        null=True))

ORDER_CLASS.add_to_class('products', models.ManyToManyField(PRODUCT_CLASS,
                                        through=ORDER_PRODUCTS_CLASS,
                                        related_name='products',
                                        verbose_name=_('products')))

ORDER_CLASS.add_to_class('user', models.ForeignKey(User,
                                        verbose_name=_('user')))

ORDER_PRODUCTS_CLASS.add_to_class('order', models.ForeignKey(ORDER_CLASS,
                                        verbose_name=_('order'),
                                        related_name='ordered_items'))

ORDER_PRODUCTS_CLASS.add_to_class('product', models.ForeignKey(PRODUCT_CLASS, 
                                        verbose_name=_('product')))

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
        
        now = datetime.datetime.now()
        hour_from = datetime.datetime(now.year, now.month, now.day, now.hour)
        hour_till = hour_from + datetime.timedelta(hours=1)

        today_orders = ORDER_CLASS.objects.filter(Q(created_at__gte=hour_from),
                            Q(created_at__lt=hour_till))

        today_orders_nums = [0]
        for o in today_orders:
            
            num = str(o.number)[8:]
            try:
                today_orders_nums.append(int(num))
            except ValueError:
                today_orders_nums.append(max(today_orders_nums))

        num = max(today_orders_nums) + 1
        instance.number = "%s%s" % (now.strftime("%y%m%d%H"), num)

post_save.connect(get_categories, sender=CATEGORY_CLASS)