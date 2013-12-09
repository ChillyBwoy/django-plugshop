# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save

from plugshop.utils import is_default_model


class CategoryAbstract(models.Model):

    name = models.CharField(_(u'name'), max_length=140)
    slug = models.SlugField(_(u'slug'), unique=True)

    class Meta:
        abstract = True
        verbose_name = _(u'category')
        verbose_name_plural = _(u'categories')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('plugshop:category', None, {'slug': self.slug})


if is_default_model('Category'):

    class Category(CategoryAbstract):

        class Meta:
            verbose_name = _(u'category')
            verbose_name_plural = _(u'categories')
            app_label = 'plugshop'
