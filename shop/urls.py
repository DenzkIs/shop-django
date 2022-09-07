from django.urls import path
from shop import views
from shop.views import (
    PrinterDetailView,
    BwPrintersListView,
    ColorPrintersListView
)


urlpatterns = [
    path('', views.home, name='shop-home'),
    path('printer/<slug>/', PrinterDetailView.as_view(), name='printer-detail'),
    path('bw-printers/', BwPrintersListView.as_view(), name='bw-printers'),
    path('color-printers/', ColorPrintersListView.as_view(), name='color-printers'),
]