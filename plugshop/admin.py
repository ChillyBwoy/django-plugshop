#encoding: utf-8
import plugshop.utils as utils

from django.contrib import admin
from django.utils.translation import ugettext as _

from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.admin import AdminImageMixin

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

class BaseGroupAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    prepopulated_fields = {
        'slug': ('name', )
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

class BaseOrderAdmin(admin.ModelAdmin):
    inlines = (
        BaseOrderProductsInline,
    )
admin.site.register(load_class(settings.ORDER_MODEL), BaseOrderAdmin)