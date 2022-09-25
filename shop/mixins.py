from django.views.generic import View
from shop.models import *
from users.models import *

#
# class CartMixin(View):
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             customer = Profile.objects.filter(user=request.user).first()
#             cart = Cart.objects.filter(owner=customer, in_order=False).first()
#             if cart:
#                 return cart
#             else:
#                 cart = Cart.objects.create(owner=customer)
#                 return cart
#         else:
#             cart = Cart.objects.filter(for_anon_user=True).first()
#             if cart:
#                 return cart
#             else:
#                 cart = Cart.objects.create(for_anon_user=True)
#                 return cart