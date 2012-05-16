#encoding: utf-8
import plugshop.utils as utils

from django.contrib import admin
from django.utils.translation import ugettext as _

from mptt.admin import MPTTModelAdmin

from plugshop import settings
from plugshop.utils import load_class
from plugshop.models import *
from plugshop.utils import is_default_model

class BaseProductAdmin(admin.ModelAdmin):
    inlines = ()
    prepopulated_fields = {
        'slug': ('name',) 
    }
    list_display = (
        'name',
        'slug',
        'category',
    )
    list_filter = (
        'category',
    )

if is_default_model('PRODUCT'):
    admin.site.register(load_class(settings.PRODUCT_MODEL), BaseProductAdmin)

class BaseCategoryAdmin(MPTTModelAdmin):
    change_list_template = 'admin/category/change_list.html'
    mptt_level_indent = 20
    prepopulated_fields = {
        'slug': ('name', )
    }
    list_display = (
        'name',
        'slug',
    )
if is_default_model('CATEGORY'):
    admin.site.register(load_class(settings.CATEGORY_MODEL), BaseCategoryAdmin)


class BaseShippingTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
    )
if is_default_model('SHIPPING_TYPE'):
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
        'updated_at',
        'delivered_at',
    )
    list_editable = (
        'status',
    )
    list_filter = (
        'status', 
    )
if is_default_model('ORDER'):
    admin.site.register(load_class(settings.ORDER_MODEL), BaseOrderAdmin)
