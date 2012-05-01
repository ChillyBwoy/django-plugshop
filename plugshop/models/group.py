# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext as _

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from plugshop import settings
from plugshop.utils import load_class

GROUP_CACHE = []

class GroupAbstractManager(TreeManager):
    def get_by_path(self, path):
        path_patterns = path.split('/')
        slug = path_patterns[-1]
        return self.get(slug=slug)

class GroupAbstract(MPTTModel):
    
    objects = GroupAbstractManager()
    
    class Meta:
        abstract = True
        verbose_name = _('Product group')
        verbose_name_plural = _('Product groups')

    class MPTTMeta:
        ordering = ['pk', 'lft']

    parent = TreeForeignKey('self', null=True, blank=True)
    name = models.CharField(blank=False, max_length=80)
    slug = models.SlugField(_('Slug'), blank=False, unique=True)

    def __unicode__(self):
        return self.name
        
    def get_path(self):
        #ancestors = self.get_ancestors(include_self=True)
        #path = "/".join([a.slug for a in ancestors])
        #return path

        nodes = GROUP_CACHE
        ancestors = [n for n in nodes 
                        if n.lft <= self.lft and 
                            n.rght >= self.rght and 
                                n.tree_id == self.tree_id]
        return "/".join([a.slug for a in ancestors])


class Group(GroupAbstract):
    class Meta:
        app_label = 'plugshop'

    @models.permalink
    def get_absolute_url(self):
        return ('PlugshopGroup', None, {'group_path': self.get_path() })

GROUP_CACHE = load_class(settings.GROUP_MODEL).objects.all()