from django.urls import path
from shop import views
from shop.views import (
    PrinterDetailView,
    BwPrintersListView,
    ColorPrintersListView,
    TonersListView,
    CartView,
    AddToCartView,

)


urlpatterns = [
    path('', views.home, name='shop-home'),
    path('stock/', views.stock, name='stock'),
    path('contact/', views.contact, name='contact'),
    path('printer/<slug>/', PrinterDetailView.as_view(), name='printer-detail'),
    path('bw-printers/', BwPrintersListView.as_view(), name='bw-printers'),
    path('color-printers/', ColorPrintersListView.as_view(), name='color-printers'),
    path('toners/', TonersListView.as_view(), name='toners'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/toner/<slug>/', AddToCartView.as_view(), name='add_to_cart'),


]