# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext as _
from plugshop.utils import load_class, is_default_model

class ShippingTypeAbstract(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('shipping type')
        verbose_name_plural = _('shipping type')

    name = models.CharField(_('name'), blank=False, max_length=100)
    price = models.PositiveIntegerField(_('price'), blank=False)
    require_address = models.BooleanField(_('require address'), 
                                            default=False)

    def __unicode__(self):
        return self.name

if is_default_model('SHIPPING_TYPE'):
    class ShippingType(ShippingTypeAbstract):
        class Meta:
            verbose_name = _('shipping type')
            verbose_name_plural = _('shipping type')
            app_label = 'plugshop'
