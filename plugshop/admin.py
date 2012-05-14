#encoding: utf-8
import plugshop.utils as utils

from django.contrib import admin
from django.utils.translation import ugettext as _

from mptt.admin import MPTTModelAdmin

from plugshop import settings
from plugshop.utils import load_class
from plugshop.models import *


class BaseProductOptionsInline(admin.TabularInline):
    model = load_class(settings.PRODUCT_OPTIONS_MODEL)
    extra = 0
    
class BaseProductAdmin(admin.ModelAdmin):
    inlines = (
        BaseProductOptionsInline,
    )
    prepopulated_fields = {
        'slug': ('name',) 
    }
    list_display = (
        'name',
        'slug',
        'is_active',
    )
    list_editable = (
        'is_active',
    )
    list_filter = (
        'is_active',
    )
admin.site.register(load_class(settings.PRODUCT_MODEL), BaseProductAdmin)

class BaseCategoryAdmin(MPTTModelAdmin):
#class BaseCategoryAdmin(admin.ModelAdmin):
    mptt_level_indent = 20
    #change_list_template = 'admin/category/change_list.html'
    prepopulated_fields = {
        'slug': ('name', )
    }
    list_display = (
        'name',
        'slug',
    )
admin.site.register(load_class(settings.CATEGORY_MODEL), BaseCategoryAdmin)

class BaseOptionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'type',
    )
admin.site.register(load_class(settings.OPTION_MODEL), BaseOptionAdmin)


class BaseShippingTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'is_default', 
    )
admin.site.register(load_class(settings.SHIPPING_TYPE_MODEL), 
                                        BaseShippingTypeAdmin)


class BaseOrderProductsInline(admin.TabularInline):
    model = load_class(settings.ORDER_PRODUCTS_MODEL)
    extra = 0
    
class BaseOrderShippingInline(admin.StackedInline):
    model = load_class(settings.SHIPPING_MODEL)
    can_delete = False

class BaseOrderAdmin(admin.ModelAdmin):
    inlines = (
        BaseOrderShippingInline,
        BaseOrderProductsInline,
    )
    list_display = (
        'id',
        'user',
        'status',
        'created_at',
        'delivered_at',
    )
    list_editable = (
        'status',
    )
    list_filter = (
        'status', 
    )
admin.site.register(load_class(settings.ORDER_MODEL), BaseOrderAdmin)