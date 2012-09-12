from django.contrib import admin

from testshop.shop.models import *

from plugshop.admin import BaseProductAdmin, BaseCategoryAdmin, BaseOrderAdmin

class CategoryAdmin(BaseCategoryAdmin):
    pass

class ProductAdmin(BaseProductAdmin):
    pass
    
class OrderAdmin(BaseOrderAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)