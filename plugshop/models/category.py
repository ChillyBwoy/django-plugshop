# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from plugshop import settings
from plugshop.utils import load_class, get_categories, is_default_model

class CategoryAbstractManager(TreeManager):
    def get_by_path(self, path):
        path_patterns = path.split('/')
        slug = path_patterns[-1]
        return self.get(slug=slug)

class CategoryAbstract(MPTTModel):

    objects = CategoryAbstractManager()

    class Meta:
        abstract = True
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    class MPTTMeta:
        ordering = ['pk', 'lft']

    parent = TreeForeignKey('self', null=True, blank=True)
    name = models.CharField(_('name'), blank=False, max_length=80)
    slug = models.SlugField(_('slug'), blank=False, unique=True)

    def __unicode__(self):
        return self.name
        
    def get_ancestor_list(self):
        categories = get_categories()
        return [n for n in categories 
                    if n.lft <= self.lft and 
                        n.rght >= self.rght and 
                            n.tree_id == self.tree_id]

    def get_path(self):
        ancestors = self.get_ancestor_list()
        return "/".join([a.slug for a in ancestors])

    @models.permalink
    def get_absolute_url(self):
        return ('plugshop-category', None, {'category_path': self.get_path() })



if is_default_model('CATEGORY'):
    class Category(CategoryAbstract):
        class Meta:
            verbose_name = _('category')
            verbose_name_plural = _('categories')
            app_label = 'plugshop'