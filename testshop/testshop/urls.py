from django.conf.urls import patterns, include, url
from shop import urls as shop_urls 

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^shop/', include('plugshop.urls')),
    #(r'^shop/', include(shop_urls)),
)
