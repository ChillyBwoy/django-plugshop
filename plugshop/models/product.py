import datetime

from django.db import models
from django.db.models import get_model
from django.utils.translation import ugettext as _

from plugshop import settings
from plugshop.utils import load_class

class ProductAbstract(models.Model):
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
        verbose_name  = _('product')
        verbose_name_plural = _('Products')

    name = models.CharField(_('Name'), blank=False, max_length=200)
    slug = models.SlugField(_('Slug'), blank=False, unique=True)
    price = models.PositiveIntegerField(_('Price'), blank=False)
    group = models.ForeignKey(load_class(settings.GROUP_MODEL), 
                                verbose_name=_('Group'),
                                blank=True)
    description  = models.TextField(_('Description'), blank=True)
    is_available = models.BooleanField(_('Is available'), default=True)
    is_active = models.BooleanField(_('Is active'), default=True)
    created_at = models.DateTimeField(_('Created at'), blank=True, null=True, 
                                        default=datetime.datetime.now)
    sort = models.PositiveSmallIntegerField(_('Sort'), default=1)

    def __unicode__(self):
        return self.name
        
    def get_path(self):
        if self.group:
            ancestors = self.group.get_ancestors()
            path = "/".join([a.slug for a in ancestors] + 
                                [self.group.slug])
        else:
            path = ""
        return path

class Product(ProductAbstract):
    class Meta:
        app_label = 'plugshop'

    @models.permalink
    def get_absolute_url(self):
        return ('PlugshopProduct', None, {
            'group_path': self.get_path(),
            'slug': self.slug,
        })