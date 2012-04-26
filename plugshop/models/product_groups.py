import datetime

from django.db import models
from django.db.models import get_model
from django.utils.translation import ugettext as _

from plugshop import settings
from plugshop.utils import load_class

class ProductGroupsAbstract(models.Model):
    class Meta:
        app_label = 'plugshop'
        abstract = True
        verbose_name = _("Product group")
        verbose_name_plural = _("Product groups")

    product = models.ForeignKey(load_class(settings.PRODUCT_MODEL))
    group = models.ForeignKey(load_class(settings.GROUP_MODEL))

class ProductGroups(ProductGroupsAbstract):
    pass