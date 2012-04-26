import datetime

from django.db import models
from django.db.models import get_model
from django.utils.translation import ugettext as _

from plugshop import settings
from plugshop.utils import load_class

OPTION_TYPE_CHOICES = (
    ('str', _('string')),
    ('int', _('integer')),
    ('text', _('text')),
    ('boolean', _('checkbox')),
    ('list', _('key-value list(key1=value1|key2=value2|...)')),
)
OPTION_TYPE_WIDGETS = (
    ('input', _('text input')),
    ('text', _('textarea')),
    ('select', _('dropdown')),
    ('radio', _('radio buttons')),
)
OPTION_TYPE_CHOICES_DEFAULT = 'str'

class OptionAbstract(models.Model):
    class Meta:
        app_label = 'plugshop'
        abstract = True
        verbose_name = _("Option")
        verbose_name_plural = _("Options")

    name = models.CharField(_('Name'), blank=False, max_length=200, 
                            unique=True)
    type = models.CharField(_('Type'), max_length=10, blank=False, 
                            choices=OPTION_TYPE_CHOICES, 
                            default=OPTION_TYPE_CHOICES_DEFAULT)

    def __unicode__(self):
        return self.name

class Option(OptionAbstract):
    pass