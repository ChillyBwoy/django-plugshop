# encoding: utf-8
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator

from django.views.generic import View, TemplateView, ListView, DetailView
from django.views.generic.base import TemplateResponseMixin

from plugshop import settings
from plugshop.utils import load_class
from plugshop.forms import *
from plugshop.cart import get_cart

PRODUCT_CLASS = load_class(settings.PRODUCT_MODEL)
GROUP_CLASS = load_class(settings.GROUP_MODEL)

class ProductListView(ListView):
    context_object_name = 'products'
    template_name = 'plugshop/product_list.html'

    def get_queryset(self):
        return PRODUCT_CLASS.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        groups = GROUP_CLASS.objects.all()
        context.update(
            groups = groups
        )
        return context

class ProductView(DetailView):
    model = PRODUCT_CLASS
    context_object_name = 'product'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        return get_object_or_404(PRODUCT_CLASS, slug=slug)

    def get_context_data(self, *args, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        product = context.get('product')
        context.update(
            group=product.group
        )
        return context


class GroupView(DetailView):
    model = GROUP_CLASS
    context_object_name = 'group'
    template_name = 'plugshop/product_list.html'

    def get_object(self, *args, **kwargs):
        path = self.kwargs.get('group_path', None)
        try:
            return GROUP_CLASS.objects.get_by_path(path)
        except GROUP_CLASS.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(GroupView, self).get_context_data(**kwargs)
        group = context.get('group')
        
        group_list = [group] + list(group.get_children())
        products = PRODUCT_CLASS.objects.filter(group__in=group_list)

        groups = GROUP_CLASS.objects.all()
        context.update(
            products = products,
            groups = groups
        )
        return context


class CartView(TemplateResponseMixin, View):
    template_name = 'plugshop/cart.html'
    
    def get_context_data(self, **kwargs):
        return {
            'cart': get_cart(self.request) or [],
        }
        
    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data.get('product')
            quantity = form.cleaned_data.get('quantity')
            cart = get_cart(request)

            cart.append(product, int(product.price), quantity)
            cart.save()

            if request.is_ajax():
                return {
                    'cart': cart
                }
            else:
                return redirect(product.get_absolute_url())
        else:
            if redirect.is_ajax():
                return {
                    'errors': form.errors
                }
            else:
                return redirect(product.get_absolute_url())

# @csrf_protect
# @render_to('cartds/cart.html')
# def cart(request):
#     cart = request.cart
# 
#     #only xhr allowed
#     if not request.is_ajax(): return redirect('shop_list')
# 
#     try:
#         delivery = Delivery.objects.filter(is_default=True)[0]
#     except IndexError:
#         delivery = None
# 
#     if delivery:
#         form = OrderForm(initial={
#             'delivery': delivery.pk
#         })
#     else:
#         form = OrderForm()
# 
#     return {
#         'cart': cart,
#         'form': form,
#         'delivery': delivery,
#         'template': 'cartds/ajax.html'
#     }
# 
# @render_to('cartds/goods.html')
# def goods(request):
#     cart = request.cart
#     return {
#         'cart': request.cart
#     }
# 
# @ajax_request
# def count(request):
#     cart = request.cart
#     count = len(cart)
#     return {
#         'count': count,
#         'label': choose_plural(count, (u'товар', u'товара', u'товаров'))
#     }
# 
# @csrf_protect
# @ajax_request
# def update(request):
#     cart = request.cart
#     
#     if len(cart) == 0: return redirect('shop_list')
#     
#     if request.method == 'POST':
#         try:
#             product = Product.objects.get(pk=request.POST.get('product', None))
# 
#             try:
#                 quantity = int(request.POST.get('quantity'))
#             except Exception:
#                 quantity = 1
# 
#             cart.remove(product, quantity)
#             cart.save()
#             context = {
#                 'cart': {
#                     'products': cart.products(),
#                     'price_total': cart.price_total(),
#                     'count': len(cart)
#                 }
#             }
#         except Product.DoesNotExist, e:
#             context = { 
#                 'errors': {
#                     'product': str(e)
#                 } 
#             }
#         return context if request.is_ajax() else redirect('cart_order')
#     else:
#         raise Http404
# 
# @csrf_protect
# @ajax_request
# def add(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST or None)
#         cart = request.cart
# 
#         if form.is_valid():
#             product = form.cleaned_data['product']
#             cart.append(product)
#             cart.save()
#             if request.is_ajax():
#                 return {
#                     'cart': {
#                         'products': cart.products(),
#                         'price_total': cart.price_total(),
#                         'count': len(cart)
#                     }
#                 }
#             else:
#                 return redirect('cart_order')
#         else:
#             return { 'errors': form.errors } if request.is_ajax() else redirect('cart_order')
#     else:
#         raise Http404
# 
# 
# @csrf_protect
# @ajax_request
# def remove(request):
#     cart = request.cart
# 
#     if request.method == 'POST':
#         try:
#             product = Product.objects.get(pk=request.POST.get('product', None))
#             cart.remove(product)
#             cart.save()
#             context = {
#                 'cart': {
#                     'products': cart.products(),
#                     'price_total': cart.price_total(),
#                     'count': len(cart)
#                 }
#             }
#         except Product.DoesNotExist, e:
#             context = { 
#                 'errors': {
#                     'product': str(e)
#                 } 
#             }
#         if request.is_ajax():
#             return context
#         else:
#             return redirect('cart_order')
#     else:
#         raise Http404
# 
# 
# 
# 
# @csrf_protect
# @render_to('cartds/cart.html')
# def order(request):
#     cart = request.cart
#     
#     #if cart is empty, then say goodbye
#     if len(cart) == 0: return redirect('shop_list')
# 
#     try:
#         delivery = Delivery.objects.filter(is_default=True)[0]
#     except IndexError:
#         delivery = None
# 
#     context = {
#         'cart': cart,
#         'template': 'base.html'
#     }
#     if request.method == 'POST':
#         form = OrderForm(request.POST, initial=request.POST)
#         context.update(form=form)
# 
#         try:
#             delivery = Delivery.objects.get(pk=int(form.data.get('delivery')))
#         except Exception, e:
#             pass
# 
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
# 
#             #if no user was found, then create it
#             try:
#                 user = User.objects.get(email=email)
#             except User.DoesNotExist:
#                 user, created = User.objects.get_or_create(
#                     username = email,
#                     first_name = form.cleaned_data.get('first_name', ''),
#                     last_name = form.cleaned_data.get('last_name', ''),
#                     is_active = True,
#                     email = form.cleaned_data.get('email')
#                 )
# 
#             try:
#                 profile = user.get_profile()
#             except Profile.DoesNotExist:
#                 profile = Profile.objects.create(user=user)
# 
#             profile.phone = form.cleaned_data.get('phone')
#             profile.save()
# 
#             order = Order.objects.create(
#                 user = user,
#                 comment = form.cleaned_data.get('comment', '')
#             )
#             order.save()
# 
#             #create delivery item with address or None
#             delivery_item = OrderDelivery.objects.create(
#                 order = order,
#                 delivery = form.cleaned_data.get('delivery'),
#                 address = form.cleaned_data.get('address')
#             )
#             delivery_item.save()
# 
#             #add products to order
#             for d in cart:
#                 order_item = OrderProduct.objects.create(
#                     order = order,
#                     product = d.product,
#                     quantity = d.quantity
#                 )
#                 order_item.save()
# 
#             message_html = render_to_string('mail/user_order.html', {
#                 'cart': cart,
#                 'address': form.cleaned_data.get('address', ''),
#                 'phone': form.cleaned_data.get('phone'),
#                 'num': order.num
#             })
#             message_text = strip_tags(message_html)
#             msg = EmailMultiAlternatives(_(u'Заказ на сайте deathstar.ru'), message_text, 'noreply@deathstar.ru', [user.email])
#             msg.attach_alternative(message_html, 'text/html')
#             msg.send()
# 
#             message_html = render_to_string('mail/new_order.html', {
#                 'cart': cart,
#                 'address': form.cleaned_data.get('address', ''),
#                 'phone': form.cleaned_data.get('phone'),
#                 'user': user,
#                 'comment': form.cleaned_data.get('comment', ''),
#                 'num': order.num
#             })
#             message_text = strip_tags(message_html)
#             mail_managers(_(u'Новый заказ на сайте deathstar.ru'), message_text, html_message=message_html)
#             mail_admins(_(u'Новый заказ на сайте deathstar.ru'), message_text, html_message=message_html)
# 
#             cart.empty()
#             cart.save()
# 
#             messages.info(request, _(u"Ваш заказ оформлен. Письмо с инструкциями выслано на адрес %(email)s") % {'email': user.email})
#             return redirect('shop_list')
#     else:
# 
#         if delivery:
#             form = OrderForm(initial={
#                 'delivery': delivery.pk
#             })
#         else:
#             form = OrderForm()
# 
#     context.update(form=form, delivery=delivery)
#     return context