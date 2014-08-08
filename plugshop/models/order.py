# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from plugshop import settings
from plugshop.utils import is_default_model, get_model


class OrderAbstract(models.Model):

    user = models.ForeignKey(User, related_name='orders',
                             verbose_name=_('user'))
    number = models.CharField(_('order number'), unique=True, blank=False,
                              null=False, max_length=10, editable=False)
    status = models.IntegerField(_('order status'), blank=False,
                                 choices=settings.STATUS_CHOICES,
                                 default=settings.STATUS_CHOICES_START)
    created_at = models.DateTimeField(_('creation date'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    delivered_at = models.DateTimeField(_('delivery date'), blank=True,
                                        null=True, editable=False)
    products = models.ManyToManyField(settings.PRODUCT_MODEL,
                                      through=settings.ORDER_PRODUCTS_MODEL,
                                      related_name='products',
                                      verbose_name=_('products'))

    class Meta:
        abstract = True
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def price_total(self):
        model = get_model(settings.ORDER_PRODUCTS_MODEL)
        items = model.objects.filter(order=self)
        return sum(item.quantity * item.product.price for item in items)
    price_total.short_description = _('Total price')

    def __unicode__(self):
        return str(self.pk)

    @models.permalink
    def get_absolute_url(self):
        return ('plugshop-order', None, {'number': self.number})


if is_default_model('ORDER'):
    class Order(OrderAbstract):

        class Meta:
            ordering = ['-created_at']
            verbose_name = _('order')
            verbose_name_plural = _('orders')
            app_label = 'plugshop'
