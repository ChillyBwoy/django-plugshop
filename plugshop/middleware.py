# -*- coding: utf-8 -*-

from plugshop import settings
from plugshop.cart import Cart


class CartMiddleware(object):

    def process_request(self, request):
        setattr(request, settings.REQUEST_NAMESPACE,
                Cart(request, settings.SESSION_NAMESPACE))

    def process_response(self, request, response):
        if hasattr(request, settings.REQUEST_NAMESPACE):
            cart = getattr(request, settings.REQUEST_NAMESPACE)
            cart.save()
        return response
