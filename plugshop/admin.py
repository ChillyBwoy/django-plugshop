# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from plugshop import settings
from plugshop.utils import is_default_model, get_model


class BaseProductAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    prepopulated_fields = {
        'slug': ('name',) 
    }
    list_display = (
        'name',
        'slug',
        'price',
        'category',
    )
    list_filter = (
        'category',
    )

if is_default_model('PRODUCT'):
    admin.site.register(get_model(settings.PRODUCT_MODEL), BaseProductAdmin)


class BaseCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name', )
    }
    list_display = (
        'name',
    )

if is_default_model('CATEGORY'):
    admin.site.register(get_model(settings.CATEGORY_MODEL), BaseCategoryAdmin)


class BaseOrderProductsInline(admin.TabularInline):
    model = get_model(settings.ORDERPRODUCTS_MODEL)
    extra = 0


class BaseOrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    inlines = (
        BaseOrderProductsInline,
    )
    search_fields = ('number', 'user',)
    list_display = (
        'number',
        'user',
        'status',
        'price_total',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'status', 
        'created_at',
    )


if is_default_model('ORDER'):
    admin.site.register(get_model(settings.ORDER_MODEL), BaseOrderAdmin)
