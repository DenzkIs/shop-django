from django.urls import path
from shop.views import (

    PrinterDetailView,
    BwPrintersListView,
    ColorPrintersListView,
    TonersListView,
    CartView,
    AddToCartView,
    HomeListView,

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


]