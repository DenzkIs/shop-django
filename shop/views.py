from django.shortcuts import render
from shop.models import *
from django.views.generic import DetailView, ListView


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
    #queryset = Printer.objects.filter(color=True)
    template_name = 'shop/toners.html'
    context_object_name = 'toners'

def home(request):
    return render(
        request,
        'shop/home.html',
        {
            'printers': Printer.objects.all(),
        }
    )


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
