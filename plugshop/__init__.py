# -*- coding: utf-8 -*-

import datetime

from django.db.models import Q

from plugshop import settings
from plugshop.utils import get_categories, get_model

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

PRODUCT_CLASS = get_model(settings.PRODUCT_MODEL)
CATEGORY_CLASS = get_model(settings.CATEGORY_MODEL)
ORDER_CLASS = get_model(settings.ORDER_MODEL)
ORDER_PRODUCTS_CLASS = get_model(settings.ORDER_PRODUCTS_MODEL)


@receiver(pre_save, sender=ORDER_CLASS)
def set_delivered(sender, instance, **kwargs):
    if instance.status == settings.STATUS_CHOICES_FINISH:
        instance.delivered_at = datetime.datetime.now()
    else:
        instance.delivered_at = None


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
        instance.number = u"%s%s" % (now.strftime('%y%m%d%H'), num)

post_save.connect(get_categories, sender=CATEGORY_CLASS)
