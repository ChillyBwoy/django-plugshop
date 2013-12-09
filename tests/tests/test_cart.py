# -*- coding: utf-8 -*-

from django.test import TestCase

from plugshop.cart import Cart, CartItem


class CartTest(TestCase):
    
    def setUp(self):
        pass
        
    def test_cart_creation(self):
        storage = {}
        cart = Cart(storage, 'test_cart')