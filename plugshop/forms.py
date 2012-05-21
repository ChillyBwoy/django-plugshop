from django import forms
from django.utils.translation import ugettext as _

from plugshop import settings
from plugshop.utils import load_class

PRODUCT_CLASS = load_class(settings.PRODUCT_MODEL)
SHIPPING_TYPE_CLASS = load_class(settings.SHIPPING_TYPE_MODEL)


NAME_ERROR = _('Name is required')
EMAIL_ERROR = _('Invalid email address')
ADDRESS_ERROR = _('Address is required')

class ProductForm(forms.Form):
    product = forms.ModelChoiceField(queryset=PRODUCT_CLASS.objects)
    quantity = forms.IntegerField(required=False)


class OrderForm(forms.Form):
    name = forms.CharField(required=True, 
                                error_messages={
                                    'required': NAME_ERROR
                                }, 
                                initial="Vasya")
    first_name = forms.CharField(required=False) 
    last_name  = forms.CharField(required=False)
    email = forms.EmailField(required=True, 
                                error_messages={
                                    'required': EMAIL_ERROR
                                }, 
                                initial="")
    shipping_type = forms.ModelChoiceField(
                                empty_label=None,
                                queryset=SHIPPING_TYPE_CLASS.objects)
    address = forms.CharField(widget=forms.widgets.Textarea(), 
                                required=False, 
                                initial="")
    products = forms.ModelMultipleChoiceField(
                                queryset=PRODUCT_CLASS.objects,
                                required=True)

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
            raise forms.ValidationError(NAME_ERROR)
        return name

    def clean_address(self):
        cleaned_data = self.cleaned_data
        shipping_type = cleaned_data.get('shipping_type')
        address = cleaned_data.get('address', '').strip()

        if shipping_type:
            if shipping_type.address_required:
                if len(address) == 0: 
                    raise forms.ValidationError(ADDRESS_ERROR)

        return address
