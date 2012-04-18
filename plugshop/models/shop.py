# encoding: utf-8
import datetime

from django.db import models

from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from plugshop import settings as shop_settings
from plugshop.utils import load_class

OPTION_TYPE_CHOICES = (
    ('str', _('string')),
    ('int', _('integer')),
    ('text', _('text')),
    ('boolean', _('checkbox')),
    ('list', _('key-value list(key1=value1|key2=value2|...)')),
)
OPTION_TYPE_WIDGETS = (
    ('input', _('text input')),
    ('text', _('textarea')),
    ('select', _('dropdown')),
    ('radio', _('radio buttons')),
)
OPTION_TYPE_CHOICES_DEFAULT = 'str'
STATUS_CHOICES = (
    ('created', _('Created')),
    ('aproved', _('Confirmed')),
    ('denied', _('Denied')),
    ('delivered', _('Delivered')),
)
PRODUCT_CLASS = load_class(shop_settings.PRODUCT_MODEL)

class Option(models.Model):
    class Meta:
        app_label = 'plugshop'
        verbose_name, verbose_name_plural = _("Option"), _("Options")

    name = models.CharField(_('Name'), blank=False, max_length=200, unique=True)
    type = models.CharField(_('Type'), max_length=10, blank=False, 
                                choices=OPTION_TYPE_CHOICES, 
                                default=OPTION_TYPE_CHOICES_DEFAULT)

    def __unicode__(self):
        return self.name


class ProductOption(models.Model):

    class Meta:
        app_label = 'plugshop'
        verbose_name = _("Product option")
        verbose_name_plural = _("Product options")

    product = models.ForeignKey(PRODUCT_CLASS)
    option = models.ForeignKey(Option)
    value = models.CharField(_('Value'), blank=False, max_length=200)
    sort = models.PositiveSmallIntegerField(_('Order'), default=1)

    def __unicode__(self):
        return "(%s) %s = '%s'" % (self.option.type, self.option.name,
                                    self.value)

class ShippingType(models.Model):

    class Meta:
        app_label = 'plugshop'
        verbose_name, verbose_name_plural = _('Shipping type'), _('Shipping type')

    name = models.CharField(_('Name'), blank=False, max_length=100)
    price = models.PositiveIntegerField(_('Price'), blank=False)
    is_default = models.BooleanField(_('Default'), default=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_default:
            ShippingType.objects.all().update(is_default=False)
            self.is_default = True
        return super(ShippingType, self).save(*args, **kwargs)


class ShippingAddress(models.Model):
    class Meta:
        app_label = 'plugshop'
        verbose_name, verbose_name_plural = _('Address'), _('Addresses')

    user = models.ForeignKey(User)
    address = models.TextField(_('Address'), blank=False)
    is_default = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_default:
            ShippingAddress.objects.filter(user=self.user).update(is_default=False)
            self.is_default = True
        return super(ShippingAddress, self).save(*args, **kwargs)

class Order(models.Model):
    
    class Meta:
        app_label = 'plugshop'
        verbose_name, verbose_name_plural = _('order'), _('Orders')
    
    user = models.ForeignKey(User, blank=True, related_name="ordered_by_user")
    shipping_type = models.ForeignKey(ShippingType, blank=True, 
                                verbose_name=_('Shipping type'))
    address = models.ForeignKey(ShippingAddress, blank=True)
    products = models.ManyToManyField(PRODUCT_CLASS, through="OrderProduct")
    status = models.CharField(_('Order status'), blank=False, max_length=80, 
                                choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(_('Date'), blank=False, 
                                        default=datetime.datetime.now)

    def __unicode__(self):
        return str(self.num)

    def get_quantity(self):
        return sum(p.quantity for p in self.products.select_related().all())
    get_quantity.short_description = _('Quantity')

    def get_total_price(self):
        return sum(p.product.price * p.quantity 
            for p in self.products.select_related().all())
    get_total_price.short_description = _('Total')


class OrderProduct(models.Model):

    class Meta:
        app_label = 'plugshop'
        verbose_name = _('Order product')
        verbose_name_plural = _('Order product')

    order = models.ForeignKey(Order)
    product = models.ForeignKey(PRODUCT_CLASS)
    quantity = models.PositiveIntegerField(_('Quantity'), blank=False, 
                                            null=False, default=1)

    def __unicode__(self):
        return "%s x %s" % (self.product.name, self.quantity)
        