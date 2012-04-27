import datetime
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
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
    
    user = models.ForeignKey(User, blank=True, related_name="ordered_by_user")
    shipping_type = models.ForeignKey(load_class(settings.SHIPPING_TYPE_MODEL), 
                                        blank=True, 
                                        verbose_name=_('Shipping type'))
    address = models.ForeignKey(load_class(settings.SHIPPING_ADDRESS_MODEL), 
                                    blank=True)

    status = models.CharField(_('Order status'), blank=False, max_length=80, 
                                choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(_('Date'), blank=False, 
                                        default=datetime.datetime.now)

    def __unicode__(self):
        return str(self.pk)

class Order(OrderAbstract):
    class Meta:
        app_label = 'plugshop'