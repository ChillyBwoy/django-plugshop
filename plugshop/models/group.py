# encoding: utf-8
from django.db import models
from django.db.models import get_model
from django.utils.translation import ugettext as _

from mptt.models import MPTTModel, TreeForeignKey

from plugshop import settings as shop_settings
from plugshop.utils import load_class

class GroupAbstract(MPTTModel):
    class Meta:
        abstract = True
        verbose_name = _('Product group')
        verbose_name_plural = _('Product groups')

    class MPTTMeta:
        ordering = ['pk', 'lft']

    parent = TreeForeignKey('self', null=True, blank=True)
    name = models.CharField(blank=False, max_length=80)
    slug = models.SlugField(_('Slug'), blank=False, unique=True)
    sort = models.PositiveSmallIntegerField(_('Order'), default=1)

    def __unicode__(self):
        return self.name

class Group(GroupAbstract):
    class Meta:
        app_label = 'plugshop'