# -*- coding: utf-8 -*-

from django.conf import settings as django_settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (TemplateView, ListView, DetailView, 
                                    CreateView, FormView)
from django.utils import simplejson as json
from django.utils.translation import ugettext_lazy as _

from plugshop import settings
from plugshop.cart import get_cart
from plugshop.forms import *
from plugshop.utils import (load_class, serialize_model, serialize_queryset, 
                            get_model)


PRODUCT_CLASS = get_model(settings.PRODUCT_MODEL)
CATEGORY_CLASS = get_model(settings.CATEGORY_MODEL)
ORDER_CLASS = get_model(settings.ORDER_MODEL)
ORDERPRODUCT_CLASS = get_model(settings.ORDERPRODUCT_MODEL)

ORDER_FORM_CLASS = load_class(settings.ORDER_FORM)


class ProductListView(ListView):
    context_object_name = 'products'
    template_name = 'plugshop/product_list.html'
    model = PRODUCT_CLASS


class ProductView(DetailView):
    model = PRODUCT_CLASS
    context_object_name = 'product'
    template_name = 'plugshop/product_detail.html'


class CategoryListView(ListView):
    model = CATEGORY_CLASS
    context_object_name = 'categories'
    template_name = 'plugshop/category_list.html'


class CategoryView(DetailView):
    model = CATEGORY_CLASS
    context_object_name = 'category'
    template_name = 'plugshop/category_detail.html'


class CartView(TemplateView):
    template_name = 'plugshop/cart.html'

    def extend_context(self, context):
        return context
        
    def extend_context_ajax(self, context):
        return context
    
    def get(self, request, **kwargs):
        cart = get_cart(request)
        context = {}

        if request.is_ajax():
            context['cart'] = cart.serialize()
            context = self.extend_context_ajax(context)
            return HttpResponse(json.dumps(context), 
                                content_type='application/json', **kwargs)
        else:
            context['form'] = ORDER_FORM_CLASS()
            context = self.extend_context(context)
            if len(cart) == 0:
                return redirect('plugshop:products')
            else:
                return self.render_to_response(context)


    def post(self, request, **kwargs):
        action = request.POST.get('_action', None)
        cart = get_cart(request)
        
        if action == 'remove_all':
            cart.empty()
        else:
            form = ProductForm(request.POST)

            if form.is_valid():
                product = form.cleaned_data.get('product')
                quantity = form.cleaned_data.get('quantity', 1)
                
                if action == 'add':
                    cart.append(product, int(product.price), quantity)

                elif action == 'remove':
                    cart.remove(product, quantity)

                elif action == 'remove_product':
                    cart.remove(product)

                else:
                    raise Http404
        cart.save()
        if request.is_ajax():
            return HttpResponse(json.dumps({'cart': cart.serialize()}), 
                                content_type='application/json', **kwargs)
        else:
            return redirect('plugshop-cart')



class OrderView(DetailView):
    model = ORDER_CLASS
    context_object_name = 'order'
    template_name = 'plugshop/order_detail.html'
    
    def get(self, request, **kwargs):
        result = super(OrderView, self).get(request, **kwargs)
        ctx = self.get_context_data(**kwargs)
        
        order = ctx.get('order', None)
        session_order = self.request.session.get('order', None)
        
        if order is None:
            raise Http404

        if session_order is None:
            return redirect('plugshop')

        if order.id != session_order.id:
            raise Http404
            
        try:
            del self.request.session['order']
        except KeyError:
            pass

        return result

    def get_object(self, *args, **kwargs):
        user = self.request.user
        number = self.kwargs.get('number', None)
        order = get_object_or_404(ORDER_CLASS, number=number)
        return order


class OrderCreateView(FormView):
    template_name = 'plugshop/order_form.html'
    form_class = ORDER_FORM_CLASS
    
    def get_success_url(self):
        return '/'
        
    def get_form(self, form_class):
        return form_class(**self.get_form_kwargs())
        
    def get(self, request, **kwargs):
        cart = get_cart(request)
        if len(cart) == 0:
            return redirect('plugshop')
        else:
            return super(OrderCreateView, self).get(request, **kwargs)

    def get_initial(self, *args, **kwargs):
        cart = get_cart(self.request)
        user = self.request.user
        initial = {}
        if user.is_authenticated():
            initial.update({
                'name': "%s %s" % (user.first_name, user.last_name),
                'email': user.email
            })
        return initial

    def get_form_kwargs(self):
        cart = get_cart(self.request)
        form_kwargs = super(OrderCreateView, self).get_form_kwargs()
        return form_kwargs

    def form_valid(self, form):
        from plugshop.signals import order_create
        
        cart = get_cart(self.request)
        if len(cart) == 0:
            raise Http404
        order = form.save(cart=cart)
        cart.empty()
        self.request.session['order'] = order

        order_create.send(sender=self, order=order, request=self.request)
        return redirect(order.get_absolute_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))