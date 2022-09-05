from django.shortcuts import render
from shop.models import *


def home(request):
    return render(
        request,
        'shop/home.html',
        {
            'printers': Printer.objects.all(),
        }
    )
