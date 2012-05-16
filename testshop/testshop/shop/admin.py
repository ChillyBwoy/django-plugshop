from django.contrib import admin

from testshop.shop.models import *

from plugshop.admin import BaseProductAdmin, BaseCategoryAdmin

class CategoryAdmin(BaseCategoryAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
admin.site.register(ShippingType)