import datetime
from django.db import models
from django.db.models.signals import post_save, pre_save

from django.dispatch import receiver

from django.contrib.auth.models import User
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
        
    user = models.ForeignKey(User)

    status = models.CharField(_('Order status'), blank=False, max_length=80, 
                                choices=STATUS_CHOICES, 
                                default='created')

    comment = models.TextField(_('Comment'), blank=True, null=True)
                                
    created_at = models.DateTimeField(_('Creation date'), blank=False, 
                                        default=datetime.datetime.now)

    delivered_at = models.DateTimeField(_('Delivery date'), blank=True, 
                                        null=True)

    def get_user(self):
        return self.address.user
    
    def __unicode__(self):
        return str(self.pk)

class Order(OrderAbstract):
    class Meta:
        app_label = 'plugshop'

# @receiver(post_save, sender=load_class(settings.ORDER_MODEL))
# def create_shipping(sender, instance, created, **kwargs):
#     if created:
#         SHIPPING_CLASS = load_class(settings.SHIPPING_MODEL)
#         SHIPPING_TYPE_CLASS = load_class(settings.SHIPPING_TYPE_CLASS)
# 
#         s, s_created = SHIPPING_CLASS.objects.get_or_create(order=instance)