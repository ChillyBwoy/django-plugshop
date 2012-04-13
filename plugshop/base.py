import datetime
from django.db import models
from django.utils.translation import ugettext as _

from django.db import models
from django.db.models import get_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from plugshop.models import Option

class ProductAbstract(models.Model):
    """docstring for Product"""

    class Meta:
        abstract = True
        verbose_name, verbose_name_plural = _('product'), _('Products')
        ordering = ['-created_at']

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