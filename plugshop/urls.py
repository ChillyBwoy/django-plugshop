# encoding: utf-8
from django.conf import settings
from django.conf.urls.defaults import *

from plugshop.views import *

urlpatterns = patterns('plugshop.views',
    url(r'^$', ProductListView.as_view(), name='PlugshopProductList'),

    url(r'^cart/$', CartView.as_view(), 
            name="PlugshopCart"),

    url(r'^(?P<group_path>[\-\/\w]+)/$', GroupView.as_view(), 
            name='PlugshopGroup'),
    url(r'^(?P<group_path>[\-\/\w]+)/(?P<slug>[\-\/\w]+)$', 
            ProductView.as_view(), 
            name='PlugshopProduct'),
)