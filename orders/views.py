from django.shortcuts import render
from django.views import View



class CreateOrderView(View):
    
    def get(self, request, *args, **kwargs):
        cart_items = []
        return render(request, 'shop/checkout.html', {"cart_items": cart_items})