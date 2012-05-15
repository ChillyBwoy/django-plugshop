# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache

from django.db.models.signals import post_save

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from plugshop import settings
from plugshop.utils import load_class

class CategoryAbstractManager(TreeManager):
    def get_by_path(self, path):
        path_patterns = path.split('/')
        slug = path_patterns[-1]
        try:
            return self.get(slug=slug)
        except ObjectDoesNotExist:
            raise load_class(settings.CATEGORY_MODEL).DoesNotExist

class CategoryAbstract(MPTTModel):

    objects = CategoryAbstractManager()

    class Meta:
        abstract = True
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    class MPTTMeta:
        ordering = ['pk', 'lft']

    parent = TreeForeignKey('self', null=True, blank=True)
    name = models.CharField(blank=False, max_length=80)
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

class Category(CategoryAbstract):
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        app_label = 'plugshop'

    @models.permalink
    def get_absolute_url(self):
        return ('plugshop-category', None, {'category_path': self.get_path() })


CATEGORY_CLASS = load_class(settings.CATEGORY_MODEL)
def get_categories(*args, **kwargs):
    categories = cache.get('plugshop_categories')
    if categories is None:
        categories = CATEGORY_CLASS.objects.all()
        cache.set('plugshop_categories', categories)
    return categories
post_save.connect(get_categories, sender=CATEGORY_CLASS)