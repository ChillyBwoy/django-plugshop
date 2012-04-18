import datetime

from django.db import models
from django.db.models import get_model
from django.utils.translation import ugettext as _

from plugshop import settings
from plugshop.utils import load_class

class ProductAbstract(models.Model):
    class Meta:
        app_label = 'plugshop'
        abstract = True
        ordering = ['-created_at']
        verbose_name  = _('product')
        verbose_name_plural = _('Products')

    groups = models.ManyToManyField(load_class(settings.GROUP_MODEL), 
                                    blank=True)
    name = models.CharField(_('Name'), blank=False, max_length=200)
    slug = models.SlugField(_('Slug'), blank=False, unique=True)
    description  = models.TextField(_('Description'), blank=True)
    price = models.PositiveIntegerField(_('Price'), blank=False)
    is_available = models.BooleanField(_('Is available'), default=True)
    is_active = models.BooleanField(_('Is active'), default=True)
    created_at = models.DateTimeField(_('Created at'), blank=True, null=True, 
                                        default=datetime.datetime.now)
    sort = models.PositiveSmallIntegerField(_('Order'), default=1)
    options = models.ManyToManyField(load_class(settings.OPTION_MODEL),
                            through=load_class(settings.PRODUCT_OPTIONS_MODEL),
                            related_name="product_options",
                            verbose_name=_('Product options'))

    def __unicode__(self):
        return self.name

class Product(ProductAbstract):
    pass