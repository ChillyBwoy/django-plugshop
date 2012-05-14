import datetime

from django.db import models
from django.db.models import get_model
from django.utils.translation import ugettext as _

from plugshop import settings
from plugshop.utils import load_class


class ProductOptionsAbstract(models.Model):
    class Meta:
        abstract = True
        verbose_name = _("product option")
        verbose_name_plural = _("product options")

    product = models.ForeignKey(load_class(settings.PRODUCT_MODEL))
    option = models.ForeignKey(load_class(settings.OPTION_MODEL))
    value = models.CharField(_('value'), blank=False, max_length=200)
    sort = models.PositiveSmallIntegerField(_('sort'), default=1)

    def __unicode__(self):
        return "(%s) %s = '%s'" % (self.option.type, self.option.name,
                                    self.value)

class ProductOptions(ProductOptionsAbstract):
    class Meta:
        app_label = 'plugshop'
        verbose_name = _("product option")
        verbose_name_plural = _("product options")