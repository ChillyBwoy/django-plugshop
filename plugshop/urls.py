# encoding: utf-8
from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from plugshop import settings
from plugshop.views import *
from plugshop.exceptions import NoUrlFound

PREFIX = settings.URL_PREFIX

urlpatterns = patterns('plugshop.views',
    url(r'^$', ProductListView.as_view(), name='plugshop'),
    url(r'^products/$', ProductListView.as_view(), name='products'),

    #categories
    url(r'^categories/$', CategoryListView.as_view(), name='categories'),
    url(r'^products/(?P<category_path>[\-\/\w]+)/$', 
        CategoryView.as_view(), name='category'),

    #products
    url(r'^products/(?P<category_slug>[\-\/\w]+)/(?P<slug>[\-\/\w]+)$', 
        ProductView.as_view(), name='product'),
        
    url(r'^cart/$', CartView.as_view(), name='cart'),
    url(r'^order/(?P<number>[\-\/\w]+)$', 
        OrderView.as_view(), name='order'),
    url(r'^order/$', OrderCreateView.as_view(), name='order-new'),
)