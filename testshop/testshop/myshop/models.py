from django.db import models
from django.utils.translation import ugettext as _

from plugshop.models import *

def get_upload_to(f, path):
    fname = f.encode('utf-8')
    md5 = hashlib.md5()
    md5.update(fname)
    path = (
        str(int(time.time())),
        md5.hexdigest(),
        fname.split('.')[-1],
    )
    return os.path.abspath(path, '.'.join(path))


# class Category(CategoryAbstract):
#     logo = models.ImageField(_('Logo'), 
#                         upload_to=lambda i,f: get_upload_to(f, 'categories'), 
#                         blank=False)
# 
# class Product(ProductAbstract):
#     discount = models.IntegerField(_('Discount'), blank=True, null=True)

# class ProductImage(models.Model):
#     product = models.ForeignKey(Product)
#     image = ImageField(_('Picture'), 
#                         upload_to=lambda i,f: get_upload_to(f, 'shop'), 
#                         blank=False)
#                         
#     is_cover = models.BooleanField(_('Is cover'), default=False)
#     sort = models.PositiveSmallIntegerField(_('Sort'), default=1)
# 
#     def save(self, *args, **kwargs):
#         if self.is_cover:
#             ProductImage.objects.filter(
#                     product=self.product
#                 ).update(is_cover=False)
#         return super(ProductImage, self).save(*args, **kwargs)