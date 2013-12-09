# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from plugshop import settings
from plugshop.utils import is_default_model


class ProductAbstract(models.Model):
    category = models.ForeignKey(settings.CATEGORY_MODEL, 
                                    verbose_name=_('category'), 
                                    related_name='products')
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True)
    price = models.PositiveIntegerField(_('price'))

    class Meta:
        abstract = True
        verbose_name  = _('product')
        verbose_name_plural = _('products')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        category = self.category
        return ('plugshop:product', None, {
            'category_slug': category.slug,
            'slug': self.slug,
        })


if is_default_model('PRODUCT'):

    class Product(ProductAbstract):
        class Meta:
            app_label = 'plugshop'
            verbose_name  = _('product')
            verbose_name_plural = _('products')