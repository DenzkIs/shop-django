from django.urls import path
from shop import views
from shop.views import PrinterDetailView


urlpatterns = [
    path('', views.home, name='shop-home'),
    path('printer/<slug>/', PrinterDetailView.as_view(), name='printer-detail'),

]