from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from plugshop import settings
from plugshop.utils import load_class, get_model

PRODUCT_CLASS = get_model(settings.PRODUCT_MODEL)
ORDER_CLASS = get_model(settings.ORDER_MODEL)
ORDER_PRODUCTS_CLASS = get_model(settings.ORDER_PRODUCTS_MODEL)
NAME_ERROR = _('Name is required')
EMAIL_ERROR = _('Invalid email address')
EMAIL_ERROR_EXISTS = _("Email address '%s' already exits, must be unique")

class ProductForm(forms.Form):
    product = forms.ModelChoiceField(queryset=PRODUCT_CLASS.objects)
    quantity = forms.IntegerField(required=False)

class OrderForm(forms.ModelForm):

    class Meta:
        model = ORDER_CLASS
        exclude = (
            'number', 
            'status',
            'created_at',
            'updated_at',
            'delivered_at',
            'user',
            'products',
        )

    name = forms.CharField(required=True, error_messages={
                                            'required': NAME_ERROR
                                        })
    email = forms.EmailField(required=True, error_messages={
                                            'required': EMAIL_ERROR
                                        })

    def save(self, commit=True, **kwargs):
        cart = kwargs.get('cart')

        user, created = User.objects.get_or_create(
            email = self.cleaned_data.get('email')
        )
        if created:
            user.username = self.cleaned_data.get('email')
            user.email = self.cleaned_data.get('email')
            user.first_name = self.cleaned_data.get('first_name', '')
            user.last_name = self.cleaned_data.get('last_name', '')
            user.is_active = False
            user.save()

        model = super(OrderForm, self).save(commit=False)
        model.user = user

        if commit:
            model.save()
            for c in cart:
                ORDER_PRODUCTS_CLASS.objects.create(
                    product=c.product,
                    quantity=c.quantity,
                    order=model
                )
                
        return model

    def clean_name(self):
        name = self.cleaned_data.get('name').strip()
        if len(name):
            n = name.split()
            if len(n) > 1:
                self.cleaned_data['first_name'] = " ".join(n[1:])
                self.cleaned_data['last_name']  = n[0]
            else:
                self.cleaned_data['first_name'] = name
                self.cleaned_data['last_name'] = ''
        else:
            raise forms.ValidationError(NAME_ERROR)
        return name