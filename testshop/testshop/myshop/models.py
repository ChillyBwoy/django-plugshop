from django.db import models
from django.utils.translation import ugettext as _
from sorl.thumbnail import ImageField

from plugshop.base import ProductAbstract

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


# class ProductGroup(ProductGroupAbstract):
#     logo = ImageField(_('Logo'), 
#                         upload_to=lambda i,f: get_upload_to(f, 'groups'), 
#                         blank=False)

class Product(ProductAbstract):
    pass

class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = ImageField(_('Picture'), 
                        upload_to=lambda i,f: get_upload_to(f, 'shop'), 
                        blank=False)
                        
    is_cover = models.BooleanField(_('Is cover'), default=False)
    sort = models.PositiveSmallIntegerField(_('Sort'), default=1)

    def save(self, *args, **kwargs):
        if self.is_cover:
            ProductImage.objects.filter(
                    product=self.product
                ).update(is_cover=False)
        return super(ProductImage, self).save(*args, **kwargs)