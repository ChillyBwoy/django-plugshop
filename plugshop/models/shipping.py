# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from mptt.models import MPTTModel, TreeForeignKey

from plugshop import settings
from plugshop.utils import load_class

class ShippingTypeAbstract(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('shipping type')
        verbose_name_plural = _('shipping type')

    name = models.CharField(_('name'), blank=False, max_length=100)
    price = models.PositiveIntegerField(_('price'), blank=False)
    is_default = models.BooleanField(_('default'), default=False)

    def __unicode__(self):
        return self.name

class ShippingType(ShippingTypeAbstract):
    class Meta:
        verbose_name = _('shipping type')
        verbose_name_plural = _('shipping type')
        app_label = 'plugshop'

class ShippingAbstract(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('shipping')
        verbose_name_plural = _('shipping list')
    
    order = models.OneToOneField(load_class(settings.ORDER_MODEL),
                            primary_key=True,
                            verbose_name=_('order'))
    type = models.ForeignKey(load_class(settings.SHIPPING_TYPE_MODEL), 
                            blank=True, null=True,
                            verbose_name=_('shipping type'))
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