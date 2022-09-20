from django.contrib import admin
from shop.models import *

admin.site.register(Printer)
admin.site.register(Category)
admin.site.register(Toner)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Order)