import datetime

from django.db import models
from django.utils.translation import ugettext as _

from plugshop import settings
from plugshop.utils import load_class

class OrderProductsAbstract(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('Order product')
        verbose_name_plural = _('Order product')

    order = models.ForeignKey(load_class(settings.ORDER_MODEL), 
                                verbose_name=_('Order'))
    product = models.ForeignKey(load_class(settings.PRODUCT_MODEL),
                                verbose_name=_('Product'))
    quantity = models.PositiveIntegerField(_('Quantity'), 
                                            blank=False, 
                                            null=False, 
                                            default=1)

class OrderProducts(OrderProductsAbstract):
    class Meta:
        app_label = 'plugshop'