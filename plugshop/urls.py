# encoding: utf-8
from django.conf import settings
from django.conf.urls.defaults import *

from plugshop.views import *

urlpatterns = patterns('plugshop.views',
    url(r'^$', ProductListView.as_view(), name='PlugshopProductList'),
    url(r'^(?P<path>[\-\/\w]+)$', GroupView.as_view(), name='PlugshopGroup'),
    url(r'^(?P<path>[\-\/\w]+)$', ProductView.as_view(), name='PlugshopProduct'),
)