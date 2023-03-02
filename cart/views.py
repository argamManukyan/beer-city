import json
from decimal import Decimal

from cart.models import Cart, CartItem
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.template.defaultfilters import floatformat
from currencies.templatetags.currency import calculate

from .context_processors import get_cart


class CartView(View):

    def get(self, request, **kwargs):
        cart = get_cart(request).get('cart')
        cart_items = cart.item.order_by('-id')
        return render(request, 'shop/cart.html', {'cart': cart, 'cart_items': cart_items})


class AddToCartView(View):

    # def post(self, request, **kwargs):
    #     data = json.loads(request.body)
    #     product_id = data.pop('product_id')
    #     quantity = data.pop('quantity')

    #     cart = get_cart(request).get('cart')
    #     data = {k: v for k, v in data.items() if v}

    #     if data != {} and cart.item.filter(product_id=product_id, features__contains=data).exists():
    #         item = cart.item.filter(product_id=product_id, features__contains=data).first()
    #         item.quantity += int(quantity)
    #         item.save()
    #     elif data == {} and cart.item.filter(product_id=product_id, features={}).exists():
    #         item = cart.item.filter(product_id=product_id, features={}).first()
    #         item.quantity += int(quantity)
    #         item.save()
    #     else:
    #         cart.item.create(product_id=product_id, features=data, quantity=quantity)
    #     cart_total = 0
    #     for i in cart.item.all():
    #         cart_total += i.item_total_price
    #     cart.cart_total = cart_total
    #     cart.save()

    #     return JsonResponse({'cart_items': cart.item.count(),
    #                          'cart_total': "{:.0f}".format(
    #                              calculate(cart.cart_total, request.session['currency'], decimals=3)), },
    #                         status=200)
    def post(self, request, **kwargs):
        data = json.loads(request.body)
        product_id = data.pop('product_id')
        quantity = data.pop('quantity')
        values = ','.join(list(filter(lambda x: int(x) > 0, data.values())))
        cart: Cart = get_cart(request).get('cart')

        if cart.item.filter(product_id=product_id, features=values).exists():
            item = cart.item.filter(product_id=product_id, features__contains=values).first()
            from shop.models import Product
            if product := Product.objects.filter(id=product_id, stored_quantity__gt=0):
                if item.quantity + int(quantity) > product.first().stored_quantity:
                    return HttpResponse(status=400)
            item.quantity += int(quantity)
            item.save()
        else:
            cart.item.create(product_id=product_id, features=values, quantity=quantity)
        cart_total = sum(i.item_total_price for i in cart.item.all())
        cart.cart_total = cart_total
        cart.save()

        return JsonResponse({
            'cart_items': cart.item.count(),
            'cart_total': "{:.0f}".format(
                calculate(cart.cart_total, request.session['currency'], decimals=3)
            ),
            }, status=200)

class RemoveFromBAsketView(View):

    def post(self, request):
        data = json.loads(request.body)

        item_id = data.get('id')
        cart = get_cart(request).get('cart')

        try:
            cart_item = CartItem.objects.get(id=item_id)
        except:
            return HttpResponse(status=400)

        cart_item.delete()

        cart_total = 0
        for i in cart.item.all():
            cart_total += i.item_total_price
        cart.cart_total = cart_total
        cart.save()

        return JsonResponse(
            {'cart_total': "{:.1f}".format(calculate(cart.cart_total, request.session['currency'], decimals=3)),
             'items_count': cart.item.count()}, status=200)


class ChangeQuantityBasketView(View):

    def post(self, request):
        data = json.loads(request.body)

        item_id = data.get('id')
        quantity = data.get('quantity')
        cart = get_cart(request).get('cart')

        try:
            cart_item = CartItem.objects.get(id=item_id)
        except:
            return HttpResponse(status=400)

        cart_item.quantity = int(quantity)
        cart_item.save()
        cart_total = 0
        for i in cart.item.all():
            cart_total += i.item_total_price
        cart.cart_total = cart_total
        cart.save()
        return JsonResponse({'cart_total': "{:.0f}".format(calculate(cart.cart_total,
                                                                     request.session['currency'],
                                                                     decimals=3)),
                             'item_total': "{:.0f}".format(calculate(cart_item.item_total_price,
                                                                     request.session['currency'],
                                                                     decimals=3))},
                            status=200)
