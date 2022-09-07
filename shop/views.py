from django.shortcuts import render
from shop.models import *
from django.views.generic import DetailView, ListView


class PrinterDetailView(DetailView):
    model = Printer


class BwPrintersListView(ListView):
    model = Printer
    queryset = Printer.objects.filter(color=False)
    template_name = 'shop/bw_printers.html'
    context_object_name = 'printers'


class ColorPrintersListView(ListView):
    model = Printer
    queryset = Printer.objects.filter(color=True)
    template_name = 'shop/color_printers.html'
    context_object_name = 'printers'


def home(request):
    return render(
        request,
        'shop/home.html',
        {
            'printers': Printer.objects.all(),
        }
    )
