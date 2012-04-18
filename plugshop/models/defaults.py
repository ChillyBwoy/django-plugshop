# from plugshop.models.base import ProductAbstract, ProductGroupAbstract
# 
# class ProductGroup(ProductGroupAbstract):
#     class Meta: 
#         app_label = 'plugshop'
# 
# class Product(ProductAbstract):
#     class Meta: 
#         app_label = 'plugshop'


class Option(models.Model):
    pass

class ProductGroup(MPTTModel):
    pass

class ProductAbstract(models.Model):
    pass
    
class ProductOptionAbstract(models.Model):
    pass