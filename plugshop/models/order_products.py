from django.db import models
from django.utils.translation import ugettext as _

class OrderProductsAbstract(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('order product')
        verbose_name_plural = _('order product')

    quantity = models.PositiveIntegerField(_('quantity'), 
                                            blank=False, 
                                            null=False, 
                                            default=1)

class OrderProducts(OrderProductsAbstract):
    class Meta:
        app_label = 'plugshop'
        verbose_name = _('order product')
        verbose_name_plural = _('order product')