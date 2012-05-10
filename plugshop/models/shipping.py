# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext as _

from mptt.models import MPTTModel, TreeForeignKey

from plugshop import settings
from plugshop.utils import load_class

class ShippingTypeAbstract(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('Shipping type')
        verbose_name_plural = _('Shipping type')

    name = models.CharField(_('Name'), blank=False, max_length=100)
    price = models.PositiveIntegerField(_('Price'), blank=False)
    is_default = models.BooleanField(_('Default'), default=False)

    def __unicode__(self):
        return self.name

class ShippingType(ShippingTypeAbstract):
    class Meta:
        app_label = 'plugshop'

class ShippingAbstract(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('Shipping address')
        verbose_name_plural = _('Shipping address list')
    
    order = models.OneToOneField(load_class(settings.ORDER_MODEL),
                            primary_key=True,
                            verbose_name=_('Order'))
    type = models.ForeignKey(load_class(settings.SHIPPING_TYPE_MODEL), 
                            blank=True, null=True,
                            verbose_name=_('Shipping type'))
    address = models.TextField(_('Address'), blank=True, null=True)
    

class Shipping(ShippingAbstract):
    class Meta:
        app_label = 'plugshop'