# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from plugshop import settings
from plugshop.utils import load_class

class ShippingAbstract(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('shipping')
        verbose_name_plural = _('shipping list')

    order = models.OneToOneField(load_class(settings.ORDER_MODEL),
                                primary_key=True,
                                related_name='shipping',
                                verbose_name=_('order'))
    address = models.TextField(_('address'), blank=True, null=True)

class Shipping(ShippingAbstract):
    class Meta:
        verbose_name = _('shipping')
        verbose_name_plural = _('shipping list')
        app_label = 'plugshop'

@receiver(post_save, sender=load_class(settings.SHIPPING_MODEL))
def remove_null_shipping(sender, instance, created, **kwargs):
    if instance.type is None:
        instance.delete()