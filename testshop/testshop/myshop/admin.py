from django.contrib import admin

from testshop.myshop.models import *
from plugshop.admin import BaseProductAdmin

# class ProductImageInline(admin.TabularInline):
#     model = ProductImage
#     extra = 0

# class ProductAdmin(BaseProductAdmin):
#     pass

# admin.site.register(Group)
#admin.site.register(Product, ProductAdmin)