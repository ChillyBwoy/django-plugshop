# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache

from django.db.models.signals import post_save
from django.dispatch import receiver

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from plugshop import settings
from plugshop.utils import load_class

class GroupAbstractManager(TreeManager):
    def get_by_path(self, path):
        path_patterns = path.split('/')
        slug = path_patterns[-1]
        try:
            return self.get(slug=slug)
        except ObjectDoesNotExist:
            raise load_class(settings.GROUP_MODEL).DoesNotExist

class GroupAbstract(MPTTModel):
    
    objects = GroupAbstractManager()
    
    class Meta:
        abstract = True
        verbose_name = _('Product group')
        verbose_name_plural = _('Product group list')

    class MPTTMeta:
        ordering = ['pk', 'lft']

    parent = TreeForeignKey('self', null=True, blank=True)
    name = models.CharField(blank=False, max_length=80)
    slug = models.SlugField(_('Slug'), blank=False, unique=True)

    def __unicode__(self):
        return self.name
        
    def get_ancestor_list(self):
        groups = get_groups()
        return [n for n in groups 
                    if n.lft <= self.lft and 
                        n.rght >= self.rght and 
                            n.tree_id == self.tree_id]

    def get_path(self):
        ancestors = self.get_ancestor_list()
        return "/".join([a.slug for a in ancestors])

class Group(GroupAbstract):
    class Meta:
        app_label = 'plugshop'

    @models.permalink
    def get_absolute_url(self):
        return ('PlugshopGroup', None, {'group_path': self.get_path() })


GROUP_CLASS = load_class(settings.GROUP_MODEL)

def get_groups(*args, **kwargs):
    groups = cache.get('plugshop_group')
    if groups is None:
        groups = GROUP_CLASS.objects.all()
        cache.set('plugshop_group', groups)
    return groups

post_save.connect(get_groups, sender=GROUP_CLASS)