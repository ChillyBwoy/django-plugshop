# encoding: utf-8
from django.conf import settings as django_settings
from django.db.models.query import QuerySet
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.core import serializers
from django.views.generic import View, TemplateView, ListView, DetailView,\
CreateView, FormView
from django.views.generic.base import TemplateResponseMixin
from django.utils import simplejson as json
from django.contrib.auth.models import User
from django.contrib import messages

from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, mail_managers, \
mail_admins

from plugshop.utils import serialize_queryset
from plugshop import settings
from plugshop.utils import load_class, serialize_model, serialize_queryset
from plugshop.forms import *
from plugshop.cart import get_cart

PRODUCT_CLASS = load_class(settings.PRODUCT_MODEL)
CATEGORY_CLASS = load_class(settings.CATEGORY_MODEL)
ORDER_CLASS = load_class(settings.ORDER_MODEL)
ORDER_PRODUCTS_CLASS = load_class(settings.ORDER_PRODUCTS_MODEL)

ORDER_FORM_CLASS = load_class(settings.ORDER_FORM)

class ProductListView(ListView):
    context_object_name = 'products'
    template_name = 'plugshop/product_list.html'
    model = PRODUCT_CLASS

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        categories = CATEGORY_CLASS.objects.all()
        context.update(
            categories = categories
        )
        return context

class ProductView(DetailView):
    model = PRODUCT_CLASS
    context_object_name = 'product'
    template_name = 'plugshop/product_detail.html'
    
    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        return get_object_or_404(PRODUCT_CLASS, slug=slug)

    def get_context_data(self, *args, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        product = context.get('product')
        context.update(
            category=product.category
        )
        return context


class CategoryView(DetailView):
    model = CATEGORY_CLASS
    context_object_name = 'category'
    template_name = 'plugshop/product_list.html'

    def get_object(self, *args, **kwargs):
        path = self.kwargs.get('category_path', None)
        try:
            return CATEGORY_CLASS.objects.get_by_path(path)
        except CATEGORY_CLASS.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        category = context.get('category')
        
        category_list = [category] + list(category.get_children())
        products = PRODUCT_CLASS.objects.filter(category__in=category_list)

        categories = CATEGORY_CLASS.objects.all()
        context.update(
            products = products,
            categories = categories
        )
        return context

class CartView(TemplateResponseMixin, View):
    template_name = 'plugshop/cart.html'

    def extend_context(self, context):
        return context
        
    def extend_context_ajax(self, context):
        return context
    
    def get(self, request, **kwargs):
        cart = request.cart
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
                return redirect('plugshop-product-list')
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



class OrderSuccessView(DetailView):
    template_name = 'plugshop/order_success.html'


class OrderView(FormView):
    template_name = 'plugshop/order_form.html'
    form_class = ORDER_FORM_CLASS
    success_url = settings.URL_SUCCESS
    
    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        return context
        
    def get_form(self, form_class):
        return form_class(**self.get_form_kwargs())

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
        form_kwargs = super(OrderView, self).get_form_kwargs()
        return form_kwargs
    
    def notify_managers(self, order):
        cart = get_cart(self.request)
        msg = render_to_string('plugshop/email/order_admin.html', {
            'cart': cart,
            'order': order,
            'total': cart.price_total(),
        })
        mail_managers(settings.MESSAGE_NEW_ORDER_ADMIN, '', html_message=msg)
        
    def notify_customer(self, order):
        cart = get_cart(self.request)
        
        msg = render_to_string('plugshop/email/order_user.html', {
            'cart': cart,
            'order': order,
            'total': cart.price_total(),
        })
        mail = EmailMessage(settings.MESSAGE_NEW_ORDER_USER, msg, 
                            django_settings.SERVER_EMAIL, 
                            [order.user.email])
        mail.content_subtype = 'html'
        mail.send()

    def form_valid(self, form):
        cart = get_cart(self.request)
        order = form.save(cart=cart)
        
        self.notify_managers(order)
        self.notify_customer(order)

        messages.info(self.request, settings.MESSAGE_SUCCESS)
        cart.empty()
        return super(OrderView, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))