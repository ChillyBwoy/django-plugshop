from django.contrib import admin

from testshop.shop.models import *

from plugshop.admin import BaseProductAdmin, BaseCategoryAdmin, BaseOrderAdmin


class CategoryAdmin(BaseCategoryAdmin):
    pass
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(BaseProductAdmin):
    pass
admin.site.register(Product, ProductAdmin)


class OrderAdmin(BaseOrderAdmin):
    pass
admin.site.register(Order, OrderAdmin)
