from django import forms
from django.utils.translation import ugettext as _

from plugshop import settings
from plugshop.utils import load_class

PRODUCT_CLASS = load_class(settings.PRODUCT_MODEL)

class ProductForm(forms.Form):
    product = forms.ModelChoiceField(queryset=PRODUCT_CLASS.objects)
    quantity = forms.IntegerField(required=True, error_messages={
                                'required': _('Quantity not specified')
                            })