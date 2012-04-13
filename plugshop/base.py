import datetime

from django.db import models
from django.db.models import get_model
from django.utils.translation import ugettext as _

from mptt.models import MPTTModel, TreeForeignKey

from plugshop import settings as shop_settings
from plugshop.utils import load_class

# class ProductGroupAbstract(MPTTModel):
#     class Meta:
#         abstract = True
#         verbose_name = _('Product group')
#         verbose_name_plural = _('Product groups')
# 
#     class MPTTMeta:
#         ordering = ['pk', 'lft']
# 
#     parent = TreeForeignKey('self', null=True, blank=True)
#     name = models.CharField(blank=False, max_length=80)
# 
#     def __unicode__(self):
#         return self.name

#GROUP_CLASS = load_class(shop_settings.GROUP_MODEL)

class ProductAbstract(models.Model):
    """docstring for Product"""
    class Meta:
        abstract = True
        verbose_name, verbose_name_plural = _('product'), _('Products')
        ordering = ['-created_at']

    #groups = models.ManyToManyField(GROUP_CLASS, blank=True)
    name = models.CharField(_('Name'), blank=False, max_length=200)
    slug = models.SlugField(_('Slug'), blank=False, unique=True)
    description  = models.TextField(_('Description'), blank=True)
    price = models.PositiveIntegerField(_('Price'), blank=False)
    is_available = models.BooleanField(_('Is available'), default=True)
    is_active = models.BooleanField(_('Is active'), default=True)
    created_at = models.DateTimeField(_('Created at'), blank=True, null=True, 
        default=datetime.datetime.now)
    sort = models.PositiveSmallIntegerField(_('Order'), default=1)

    # options = models.ManyToManyField(Option, 
    #                 through=get_model('plugshop', 'ProductOption'), 
    #                 related_name="product_options")

    def get_options(self):
        P = get_model('plugshop', 'ProductOption')
        return P.objects.filter(product=self)

    def __unicode__(self):
        return self.name