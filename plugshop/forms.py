from django import forms
from django.utils.translation import ugettext as _

from plugshop import settings
from plugshop.utils import load_class

PRODUCT_CLASS = load_class(settings.PRODUCT_MODEL)
SHIPPING_TYPE_CLASS = load_class(settings.SHIPPING_TYPE_MODEL)

class ProductForm(forms.Form):
    product = forms.ModelChoiceField(queryset=PRODUCT_CLASS.objects)
    quantity = forms.IntegerField(required=False)

class OrderForm(forms.Form):
    name = forms.CharField(required=True, error_messages={'required': _('Name required')}, initial="")
    email = forms.EmailField(required=True, error_messages={'required': _('Invalid email')}, initial="")
    phone = forms.CharField(required=True, error_messages={'required': _('Invalid phone')}, initial="")
    shipping_type = forms.ModelChoiceField(queryset=SHIPPING_TYPE_CLASS.objects)
    address = forms.CharField(widget=forms.widgets.Textarea(), required=False, initial="")
    comment = forms.CharField(widget=forms.widgets.Textarea(), required=False, initial="")

    first_name = ""
    last_name  = ""

    def clean_name(self):
        name = self.cleaned_data.get('name').strip()
        if len(name):
            n = name.split(' ')
            if len(n) > 1:
                self.cleaned_data['first_name'] = n[0]
                self.cleaned_data['last_name']  = n[1]
            else:
                self.cleaned_data['first_name'] = name
        else:
            raise forms.ValidationError(_('Name required'))
        return name

    def clean_address(self):
        cleaned_data = self.cleaned_data
        shipping_type = cleaned_data.get('shipping_type')
        address = cleaned_data.get('address', '').strip()

        # if shipping_type.require_address:
        #     if len(address) == 0: raise forms.ValidationError(_('Address required'))

        return address
