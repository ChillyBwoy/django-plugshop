# encoding: utf-8
from django import template
from django.utils.translation import ugettext as _

register = template.Library()

@register.filter
def plugshop_currency(value):
    if value is None: return ""

    v = str(value)[::-1]
    return " ".join([v[i:i+3][::-1] for i in xrange(0, len(v), 3) ][::-1])

@register.simple_tag
def plugshop_option(opt_type, value, name=None):
    if opt_type == 'str':
        return str(value)
    elif opt_type == 'int':
        return int(value)
    elif opt_type == 'list':
        try:
            choices = (v.split('=') for v in value.split('|'))
            field_name = "option[%s]" % name if name else "option[]"
            return Select().render(field_name, None, choices=choices, attrs={
                'class': 'shop-form-select'
            })
        except ValueError:
            return ""


@register.inclusion_tag('plugshop/tags/action.html')
def plugshop_action(product, action, quantity=1):
    return {
        'product': product,
        'action': action,
        'quantity': quantity,
    }
