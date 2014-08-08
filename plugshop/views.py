# -*- coding: utf-8 -*-

from django.conf import settings as django_settings
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.views.generic import View, ListView, DetailView, FormView
from django.views.generic.base import TemplateResponseMixin
from django.utils import simplejson as json
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, mail_managers

from plugshop import settings
from plugshop.utils import load_class, get_model
from plugshop.forms import *
from plugshop.cart import get_cart

PRODUCT_CLASS = get_model(settings.PRODUCT_MODEL)
CATEGORY_CLASS = get_model(settings.CATEGORY_MODEL)
ORDER_CLASS = get_model(settings.ORDER_MODEL)
ORDER_PRODUCTS_CLASS = get_model(settings.ORDER_PRODUCTS_MODEL)

ORDER_FORM_CLASS = load_class(settings.ORDER_FORM)


class ProductListView(ListView):
    context_object_name = 'products'
    template_name = 'plugshop/product_list.html'
    model = PRODUCT_CLASS

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = CATEGORY_CLASS.objects.all()
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
        context['category'] = product.category
        return context


class CategoryListView(ListView):
    model = CATEGORY_CLASS
    context_object_name = 'categories'
    template_name = 'plugshop/category_list.html'


class CategoryView(DetailView):
    model = CATEGORY_CLASS
    context_object_name = 'category'
    template_name = 'plugshop/category_detail.html'

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

        context['products'] = products
        context['categories'] = CATEGORY_CLASS.objects.all()
        return context


class CartView(TemplateResponseMixin, View):
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
                return redirect('plugshop')
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
        number = self.kwargs.get('number', None)
        order = get_object_or_404(ORDER_CLASS, number=number)
        return order


class OrderCreateView(FormView):
    template_name = 'plugshop/order_form.html'
    form_class = ORDER_FORM_CLASS

    def get_success_url(self):
        return '/'

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        return context

    def get_form(self, form_class):
        return form_class(**self.get_form_kwargs())

    def get(self, request, **kwargs):
        cart = get_cart(request)
        if len(cart) == 0:
            return redirect('plugshop')
        else:
            return super(OrderCreateView, self).get(request, **kwargs)

    def get_initial(self, *args, **kwargs):
        user = self.request.user
        initial = {}
        if user.is_authenticated():
            initial.update({
                'name': "%s %s" % (user.first_name, user.last_name),
                'email': user.email
            })
        return initial

    def get_form_kwargs(self):
        form_kwargs = super(OrderCreateView, self).get_form_kwargs()
        return form_kwargs

    def get_admin_mail_title(self, order):
        return settings.MESSAGE_NEW_ORDER_ADMIN

    def get_customer_mail_title(self, order):
        return settings.MESSAGE_NEW_ORDER_USER

    def notify_managers(self, order):
        cart = get_cart(self.request)
        msg = render_to_string('plugshop/email/order_admin.html', {
            'cart': cart,
            'order': order,
            'total': cart.price_total(),
        })
        mail_managers(self.get_admin_mail_title(order), '', html_message=msg)

    def notify_customer(self, order):
        cart = get_cart(self.request)

        msg = render_to_string('plugshop/email/order_user.html', {
            'cart': cart,
            'order': order,
            'total': cart.price_total(),
        })
        mail = EmailMessage(self.get_customer_mail_title(order), msg,
                            django_settings.SERVER_EMAIL, [order.user.email])
        mail.content_subtype = 'html'
        mail.send()

    def form_valid(self, form):
        from plugshop.signals import order_create

        cart = get_cart(self.request)
        if len(cart) == 0:
            raise Http404
        order = form.save(cart=cart)

        self.notify_managers(order)
        self.notify_customer(order)

        messages.info(self.request, settings.MESSAGE_SUCCESS)
        cart.empty()

        self.request.session['order'] = order

        order_create.send(sender=self, order=order, request=self.request)

        return redirect(order.get_absolute_url())
        #return super(OrderCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
