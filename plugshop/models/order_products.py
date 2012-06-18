from django.db import models
from django.utils.translation import ugettext as _
from plugshop.utils import is_default_model

class OrderProductsAbstract(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('order product')
        verbose_name_plural = _('order product')

    quantity = models.PositiveIntegerField(_('quantity'), blank=False, 
                                            null=False, default=1)

    def price(self):
        return self.product.price * self.quantity
    price.short_description = _('Total price')

if is_default_model('ORDER_PRODUCTS'):
    class OrderProducts(OrderProductsAbstract):
        class Meta:
            app_label = 'plugshop'
            verbose_name = _('order product')
            verbose_name_plural = _('order product')