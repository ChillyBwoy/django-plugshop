import datetime
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from plugshop import settings
from plugshop.utils import get_model, get_categories

from plugshop.models.product import *
from plugshop.models.category import *
from plugshop.models.order import *
from plugshop.models.order_products import *

post_save.connect(get_categories, sender=get_model(settings.CATEGORY_MODEL))

@receiver(pre_save, sender=get_model(settings.ORDER_MODEL))
def generate_number(sender, instance, **kwargs):
    if instance.id is None:
        now = datetime.datetime.now()
        hour_from = datetime.datetime(now.year, now.month, now.day, now.hour)
        hour_till = hour_from + datetime.timedelta(hours=1)

        order_class = get_model(settings.ORDER_MODEL)
        today_orders = order_class.objects.filter(Q(created_at__gte=hour_from),
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