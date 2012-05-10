import datetime
from django.db import models
from django.db.models.signals import post_save, pre_save

from django.dispatch import receiver

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from mptt.models import MPTTModel, TreeForeignKey

from plugshop import settings
from plugshop.utils import load_class

class OrderAbstract(models.Model):

    class Meta:
        abstract = True
        verbose_name = _('order')
        verbose_name_plural = _('Orders')

    user = models.ForeignKey(User)
    status = models.IntegerField(_('Order status'), blank=False, 
                                choices=settings.STATUS_CHOICES, 
                                default=settings.STATUS_CHOICES_START)
    created_at = models.DateTimeField(_('Creation date'), blank=False, 
                                        default=datetime.datetime.now)
    delivered_at = models.DateTimeField(_('Delivery date'), blank=True, 
                                        null=True)
    comment = models.TextField(_('Comment'), blank=True, null=True)
    
    def __unicode__(self):
        return str(self.pk)

class Order(OrderAbstract):
    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('Orders')
        app_label = 'plugshop'
        
@receiver(pre_save, sender=load_class(settings.ORDER_MODEL))
def set_delivered(sender, instance, **kwargs):
    if instance.status == settings.STATUS_CHOICES_FINISH:
        instance.delivered_at = datetime.datetime.now()
    else:
        instance.delivered_at = None