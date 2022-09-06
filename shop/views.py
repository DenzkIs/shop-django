from django.shortcuts import render
from shop.models import *
from django.views.generic import DetailView


class PrinterDetailView(DetailView):
    model = Printer

def home(request):
    return render(
        request,
        'shop/home.html',
        {
            'printers': Printer.objects.all(),
        }
    )

