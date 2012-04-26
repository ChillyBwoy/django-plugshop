#encoding: utf-8
import plugshop.utils as utils

from django.contrib import admin
from django.utils.translation import ugettext as _

from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.admin import AdminImageMixin

from plugshop import settings
from plugshop.utils import load_class
from plugshop.models import *


class BaseProductGroupsInline(admin.TabularInline):
    model = load_class(settings.PRODUCT_GROUPS_MODEL)
    extra = 0

class BaseProductOptionsInline(admin.TabularInline):
    model = load_class(settings.PRODUCT_OPTIONS_MODEL)
    extra = 0
    
class BaseProductAdmin(admin.ModelAdmin):
    inlines = (
        BaseProductGroupsInline,
        BaseProductOptionsInline,
    )
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
admin.site.register(load_class(settings.PRODUCT_MODEL), BaseProductAdmin)

class BaseGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',)
    }
    list_display = (
        'name',
        'slug',
    )
admin.site.register(load_class(settings.GROUP_MODEL), BaseGroupAdmin)


class BaseOptionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'type',
    )
admin.site.register(load_class(settings.OPTION_MODEL), BaseOptionAdmin)
    
# 
# class OptionAdmin(admin.ModelAdmin):
#     list_display = (
#         'name',
#     )
# admin.site.register(Option, OptionAdmin)
# 
# 
# class OrderProductInline(admin.TabularInline):
#     model = OrderProduct
#     extra = 0
# 
# class OrderAdmin(admin.ModelAdmin):
#     inlines = (
#         OrderProductInline,
#     )
#     search_fields = (
#         'user__email', 
#         'user__first_name', 
#         'user__last_name',
#     )
#     list_filter = (
#         'status',
#     )
#     radio_fields = (
#         {'status': admin.VERTICAL}
#     )
# admin.site.register(Order, OrderAdmin)


# class ShippingTypeAdmin(admin.ModelAdmin):
#     list_display = (
#         'name', 
#         'is_default', 
#         'price',
#     )
# admin.site.register(ShippingType, ShippingTypeAdmin)