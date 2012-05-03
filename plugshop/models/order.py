import datetime
from django.db import models
from django.utils.translation import ugettext as _
from mptt.models import MPTTModel, TreeForeignKey


from plugshop import settings
from plugshop.utils import load_class

STATUS_CHOICES = (
    ('created', _('Created')),
    ('aproved', _('Confirmed')),
    ('denied', _('Denied')),
    ('delivered', _('Delivered')),
)

class OrderAbstract(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('order')
        verbose_name_plural = _('Orders')

    shipping_type = models.ForeignKey(load_class(settings.SHIPPING_TYPE_MODEL), 
                                        blank=True, 
                                        null=True, 
                                        verbose_name=_('Shipping type'))

    address = models.ForeignKey(load_class(settings.SHIPPING_ADDRESS_MODEL), 
                                    blank=True,
                                    null=True)

    status = models.CharField(_('Order status'), blank=False, max_length=80, 
                                choices=STATUS_CHOICES, 
                                default='created')
    created_at = models.DateTimeField(_('Creation date'), blank=False, 
                                        default=datetime.datetime.now)
    # completed_at = models.DateTimeField(_('Delivery date'), blank=True, 
    #                                     null=True)

    def get_user(self):
        return self.address.user
    
    def __unicode__(self):
        return str(self.pk)

class Order(OrderAbstract):
    class Meta:
        app_label = 'plugshop'