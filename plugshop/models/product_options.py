from django.db import models
from django.utils.translation import ugettext as _
from plugshop.utils import is_default_model

class ProductOptionsAbstract(models.Model):
    class Meta:
        abstract = True
        verbose_name = _("product option")
        verbose_name_plural = _("product options")

    value = models.CharField(_('value'), blank=False, max_length=200)
    sort = models.PositiveSmallIntegerField(_('sort'), default=1)

    def __unicode__(self):
        return "(%s) %s = '%s'" % (self.option.type, self.option.name,
                                    self.value)

if is_default_model('PRODUCT_OPTIONS'):
    class ProductOptions(ProductOptionsAbstract):
        class Meta:
            app_label = 'plugshop'
            verbose_name = _("product option")
            verbose_name_plural = _("product options")