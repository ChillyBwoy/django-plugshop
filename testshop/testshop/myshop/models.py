from shop.models import Product
from django.db import models
from django.utils.translation import ugettext as _
from plugshop.base import ProductAbstract
from sorl.thumbnail import ImageField

def get_upload_to(f):
    fname = f.encode('utf-8')
    md5 = hashlib.md5()
    md5.update(fname)
    path = (
        str(int(time.time())),
        md5.hexdigest(),
        fname.split('.')[-1],
    )
    return os.path.abspath('shop', '.'.join(path))


class Group(models.Model):
    name = models.CharField(blank=False, max_length=80)
    sort = models.PositiveSmallIntegerField(_('Sort'), default=1)
    
    def __unicode__(self):
        return self.name



class Product(ProductAbstract):
    group = models.ForeignKey(Group)



class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = ImageField(_('Picture'), 
                        upload_to=lambda i,f: get_upload_to(f), 
                        blank=False)
    is_cover = models.BooleanField(_('Is cover'), default=False)
    sort = models.PositiveSmallIntegerField(_('Sort'), default=1)

    def save(self, *args, **kwargs):
        if self.is_cover:
            ProductImage.objects.filter(
                    product=self.product
                ).update(is_cover=False)
        return super(ProductImage, self).save(*args, **kwargs)