# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from plugshop import settings
from plugshop.utils import is_default_model


class OrderProductAbstract(models.Model):
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    order = models.ForeignKey(settings.ORDER_MODEL, verbose_name=_('order'),
                              related_name='ordered_items')
    product = models.ForeignKey(settings.PRODUCT_MODEL, 
                                verbose_name=_('product'))

    class Meta:
        abstract = True
        verbose_name = _('order product')
        verbose_name_plural = _('order product')

    @property
    def price(self):
        return self.product.price * self.quantity



if is_default_model('OrderProduct'):

    class OrderProduct(OrderProductAbstract):

        class Meta:
            app_label = 'plugshop'
            verbose_name = _('order product')
            verbose_name_plural = _('order product')