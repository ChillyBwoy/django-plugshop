# encoding: utf-8
from django.db import models
from django.db.models import get_model
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from mptt.models import MPTTModel, TreeForeignKey

from plugshop import settings as shop_settings
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
    
class ShippingAddressAbstract(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('Shipping address')
        verbose_name_plural = _('Shipping addresses')

    user = models.ForeignKey(User)
    address = models.TextField(_('Address'), blank=False)
    is_default = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s – %s" % (self.user, self.address)

class ShippingAddress(ShippingAddressAbstract):
    class Meta:
        app_label = 'plugshop'