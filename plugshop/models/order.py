import datetime
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from plugshop import settings
from plugshop.utils import load_class, is_default_model

class OrderAbstract(models.Model):

    class Meta:
        abstract = True
        verbose_name = _('order')
        verbose_name_plural = _('orders')
    
    number = models.IntegerField(_('order number'), unique=True, 
                                editable=False)
    status = models.IntegerField(_('order status'), blank=False, 
                                choices=settings.STATUS_CHOICES, 
                                default=settings.STATUS_CHOICES_START)
    created_at = models.DateTimeField(_('creation date'), blank=False, 
                                        default=datetime.datetime.now,
                                        editable=False)
    updated_at = models.DateTimeField(_('updated at'), blank=True, null=True,
                                        editable=False)
    delivered_at = models.DateTimeField(_('delivery date'), blank=True, 
                                        null=True,
                                        editable=False)
                                        
    def get_price(self):
        items = load_class(settings.ORDER_PRODUCTS_MODEL).objects.filter(
                                                                    order=self)
        return sum(item.quantity * item.product.price for item in items)
    
    def __unicode__(self):
        return str(self.pk)


if is_default_model('ORDER'):
    class Order(OrderAbstract):
        class Meta:
            ordering = ['-created_at']
            verbose_name = _('order')
            verbose_name_plural = _('orders')
            app_label = 'plugshop'