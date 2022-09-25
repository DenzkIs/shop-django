from django.urls import path
from shop.views import (

    PrinterDetailView,
    BwPrintersListView,
    ColorPrintersListView,
    TonersListView,
    CartView,
    AddToCartView,
    HomeListView,
    DeleteFromCartView,
    ChangeQtyView,
    CheckoutView,
    MakeOrderView,
    SearchView,

    stock,
    contact,

)


urlpatterns = [
    path('', HomeListView.as_view(), name='shop-home'),
    path('stock/', stock, name='stock'),
    path('contact/', contact, name='contact'),
    path('printer/<slug>/', PrinterDetailView.as_view(), name='printer-detail'),
    path('bw-printers/', BwPrintersListView.as_view(), name='bw-printers'),
    path('color-printers/', ColorPrintersListView.as_view(), name='color-printers'),
    path('toners/', TonersListView.as_view(), name='toners'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/toner/<slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/toner/<slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/toner/<slug>/', ChangeQtyView.as_view(), name='change_qty'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('search/', SearchView.as_view(), name='search'),

]