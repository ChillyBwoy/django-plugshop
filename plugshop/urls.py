# encoding: utf-8
from django.conf import settings
from django.conf.urls.defaults import *

from plugshop.views import *

urlpatterns = patterns('plugshop.views',
    url(r'^$', ProductListView.as_view(), name='Products'),
    url(r'^(?P<slug>[\-\w]+)$', GroupView.as_view(), name='Group'),
    url(r'^(?P<group>[\-\w]+)/(?P<slug>[\-\w]+)$', ProductView.as_view(), name='Product'),
)