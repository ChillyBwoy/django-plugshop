#encoding: utf-8
import plugshop.utils as utils

from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext as _

from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.admin import AdminImageMixin

from plugshop.models import *

class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 0

class ShippingAddressInline(admin.TabularInline):
    model = ShippingAddress
    extra = 0

class BaseProductAdmin(admin.ModelAdmin):
    class Meta:
        abstract = True

    prepopulated_fields = {
        'slug': ('name',) 
    }
    list_display = (
        'name',
        'slug',
        'is_available',
        'is_active',
    )
    list_editable = (
        'is_active',
        'is_available',
    )
    list_filter = (
        'is_available',
        'is_active',
    )





class OptionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
admin.site.register(Option, OptionAdmin)


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = (
        OrderProductInline,
    )
    search_fields = (
        'user__email', 
        'user__first_name', 
        'user__last_name',
    )
    list_filter = (
        'status',
    )
    radio_fields = (
        {'status': admin.VERTICAL}
    )
admin.site.register(Order, OrderAdmin)


class ShippingTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'is_default', 
        'price',
    )
admin.site.register(ShippingType, ShippingTypeAdmin)