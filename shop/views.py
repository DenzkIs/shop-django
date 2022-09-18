from django.shortcuts import render
from django.http import HttpResponseRedirect
from shop.models import *
from users.models import Profile
from django.views.generic import DetailView, ListView, View


class CartView(View):

    # model = Cart
    # context_object_name = 'cart'
    # template_name = 'shop/cart.html'

    def get(self, request, *args, **kwargs):
        customer = Profile.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        context = {
            'cart': cart,
        }
        return render(request, 'shop/cart.html', context)


class AddToCartView(View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        customer = Profile.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer, in_order=False)
        product = Toner.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=cart.owner, cart=cart, product_toner=product,
        )
        if created:
            cart.product.add(cart_product)
        return HttpResponseRedirect('/cart/')


class PrinterDetailView(DetailView):
    model = Printer
    context_object_name = 'printer'


class BwPrintersListView(ListView):
    model = Printer
    queryset = Printer.objects.filter(color=False)
    template_name = 'shop/printers.html'
    context_object_name = 'printers'


class ColorPrintersListView(ListView):
    model = Printer
    queryset = Printer.objects.filter(color=True)
    template_name = 'shop/printers.html'
    context_object_name = 'printers'


class TonersListView(ListView):
    model = Toner
    # queryset = Printer.objects.filter(color=True)
    template_name = 'shop/toners.html'
    context_object_name = 'toners'


class BaseView(View):

    def get(self, request, *args, **kwargs):
        customer = Profile.objects.get(user=request.user)  # содержит информацию о покупателе
        cart = Cart.objects.get(owner=customer)  # cодержит информацию о корзине покупателя
        # далее в шаблоне base.html я вывожу количество товаров в коризине {{ cart.product.count }}
        # но расширенные шаблоны через {% extends "shop/base.html" %} не знают о переменной cart
        # как правильно передать cart в base.html, т.к. там в шапке значек корзины с кол-вом товара в ней?
        # user.user_profile.cart_set.first.product.count
        return render(request, 'shop/base.html', {'cart': cart})


class HomeListView(ListView):

    model = Printer
    template_name = 'shop/home.html'
    context_object_name = 'printers'


# def home(request):
#     return render(request, 'shop/home.html', {'printers': Printer.objects.all()})


def stock(request):
    return render(
        request,
        'shop/stock.html',
        {}
    )


def contact(request):
    return render(
        request,
        'shop/contact.html',
        {}
    )
