import datetime

from django.db import models
from django.db.models import get_model
from django.core.cache import cache

from django.utils.translation import ugettext as _

from plugshop import settings
from plugshop.utils import load_class
from plugshop.models.category import get_categories

class ProductAbstract(models.Model):
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
        verbose_name  = _('product')
        verbose_name_plural = _('products')

    name = models.CharField(_('name'), blank=False, max_length=200)
    slug = models.SlugField(_('slug'), blank=False, unique=True)
    price = models.PositiveIntegerField(_('price'), blank=False)
    category = models.ForeignKey(load_class(settings.CATEGORY_MODEL), 
                                verbose_name=_('category'),
                                blank=True,
                                null=True)
    description  = models.TextField(_('description'), blank=True)
    is_available = models.BooleanField(_('is available'), default=True)
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), blank=True, null=True, 
                                        default=datetime.datetime.now)
    sort = models.PositiveSmallIntegerField(_('sort'), default=1)

    def __unicode__(self):
        return self.name

class Product(ProductAbstract):
    class Meta:
        app_label = 'plugshop'
        verbose_name  = _('product')
        verbose_name_plural = _('products')

    @models.permalink
    def get_absolute_url(self):
        categories = get_categories()
        try:
            category = filter(lambda x: x.pk == self.category_id, categories)[0]
            category_path = category.get_path()
        except IndexError:
            category_path = "-"

        return ('plugshop-product', None, {
            'category_path': category_path,
            'slug': self.slug,
        })
