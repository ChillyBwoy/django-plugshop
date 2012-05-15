# encoding: utf-8
from django import template
from django.utils.translation import ugettext as _

register = template.Library()

@register.filter
def plugshop_currency(value):
    if value is None: return ""

    v = str(value)[::-1]
    return " ".join([v[i:i+3][::-1] for i in xrange(0, len(v), 3) ][::-1])

@register.inclusion_tag('plugshop/tags/action.html')
def plugshop_action(product, action, quantity=1):
    return {
        'product': product,
        'action': action,
        'quantity': quantity,
    }
