# encoding: utf-8
from django.conf import settings
from django.conf.urls.defaults import *

from plugshop.views import *

urlpatterns = patterns('plugshop.views',
    url(r'^$', ProductListView.as_view(), name='plugshop-product-list'),
    url(r'^cart/$', CartView.as_view(), 
            name="plugshop-cart"),
    url(r'^(?P<category_path>[\-\/\w]+)/$', CategoryView.as_view(), 
            name='plugshop-category'),
    url(r'^(?P<category_path>[\-\/\w]+)/(?P<slug>[\-\/\w]+)$', 
            ProductView.as_view(), 
            name='plugshop-product'),
)