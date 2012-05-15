# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext as _

from plugshop import settings
from plugshop.utils import load_class, is_default_model

class ShippingAbstract(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('shipping')
        verbose_name_plural = _('shipping list')

    address = models.TextField(_('address'), blank=True, null=True)

if is_default_model('SHIPPING'):
    class Shipping(ShippingAbstract):
        class Meta:
            verbose_name = _('shipping')
            verbose_name_plural = _('shipping list')
            app_label = 'plugshop'