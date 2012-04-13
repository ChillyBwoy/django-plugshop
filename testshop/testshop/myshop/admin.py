from django.contrib import admin

from testshop.myshop.models import *
from plugshop.admin import BaseProductAdmin, ProductOptionInline

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

class ProductAdmin(BaseProductAdmin):
    inlines = (
        ProductOptionInline,
        ProductImageInline,
    )

admin.site.register(Group)
admin.site.register(Product, ProductAdmin)