from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from .forms import OrderForm
from shop.models import *
from users.models import Profile


class SearchView(ListView):
    template_name = 'shop/search.html'
    context_object_name = 'toners'

    def get_queryset(self):
        return Toner.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CartView(LoginRequiredMixin, View):

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


class CheckoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Profile.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        form = OrderForm(request.POST or None)
        context = {
            'cart': cart,
            'form': form,
        }
        return render(request, 'shop/checkout.html', context)


class MakeOrderView(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = Profile.objects.get(user=request.user)
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.delivery = form.cleaned_data['delivery']
            new_order.order_date = form.cleaned_data['order_date']
            cart = Cart.objects.get(owner=new_order.customer)
            new_order.comment = form.cleaned_data['comment'] + f'\n---------------------\n'

            # Данным циклом решаю несколько проблем:
            # 1) Вывожу в поле комментариев к заказу информацию о заказе.
            #    Менеджеру не придется лезть и искать корзину, связанную с заказом.
            # 2) Очищаю корзину, чтобы она отображалась как пустая.

            for i in cart.product.all():
                new_order.comment += f'{str(i.product_toner)} - {i.qty} шт. - {i.final_price} руб.\n'
                i.delete()
                cart.save()

            new_order.save()
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class AddToCartView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        customer = Profile.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        product = Toner.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=cart.owner, cart=cart, product_toner=product,
        )
        if created:
            cart.product.add(cart_product)
            cart.save()
            messages.add_message(request, messages.INFO, f"Тонер {product.title} добавлен в корзину")
        else:
            messages.add_message(request, messages.INFO, f"Тонер {product.title} уже в корзине!")
        print(request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteFromCartView(View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        customer = Profile.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        product = Toner.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=cart.owner, cart=cart, product_toner=product,
        )
        cart.product.remove(cart_product)
        cart_product.delete()
        cart.save()
        messages.add_message(request, messages.INFO, f"Тонер {product.title} удален из корзины")
        return HttpResponseRedirect('/cart/')


class ChangeQtyView(View):

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        customer = Profile.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        product = Toner.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=cart.owner, cart=cart, product_toner=product,
        )
        qty = int(request.POST.get('qty'))
        if cart_product.qty != qty:
            cart_product.qty = qty
            cart_product.save()
            cart.save()
            messages.add_message(request, messages.INFO, f"Количество тонера {product.title} измененно на {qty} шт.")
        return HttpResponseRedirect('/cart/')


class PrinterDetailView(DetailView):
    model = Printer
    context_object_name = 'printer'


class BwPrintersListView(ListView):
    model = Printer
    queryset = Printer.objects.filter(color=False)
    template_name = 'shop/printers.html'
    context_object_name = 'printers'
    paginate_by = 4
    ordering = ['-price']


class ColorPrintersListView(ListView):
    model = Printer
    queryset = Printer.objects.filter(color=True)
    template_name = 'shop/printers.html'
    context_object_name = 'printers'
    paginate_by = 4
    ordering = ['-price']


class TonersListView(ListView):
    model = Toner
    template_name = 'shop/toners_table.html'
    context_object_name = 'toners'
    paginate_by = 8
    ordering = ['title']


class HomeListView(ListView):
    model = Printer
    template_name = 'shop/home.html'
    context_object_name = 'printers'
    ordering = ['-price']


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
