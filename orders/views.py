import datetime
from typing import Callable, List, Union

from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View
from django.utils.translation import ugettext_lazy as _

from cart.context_processors import get_cart
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem, PromoCodes
from orders.service import make_bank_request, make_idram_request
from users.models import Region, State
from users.settings import CUSTOM_MESSAGES

from .forms import OrderForm


def check_promo_code(request, promo_code, view_checking=False) -> Union[tuple, JsonResponse]:
    
    promo = PromoCodes.objects.filter(name__iexact=promo_code, is_active=True)
    cart_amount = get_cart(request)['cart'].cart_total
    
    if not promo.exists():
        return helper_check_promo_code('PROMO_CODE_NOT_FOUND', request, 404, view_checking)
    promo: PromoCodes = promo.first()
    current_datetime = timezone.now() + datetime.timedelta(hours=4)

    if promo.to_date and promo.to_date < current_datetime:
        promo.is_active = False
        promo.save()
        return helper_check_promo_code('PROMO_CODE_EXPIRED', request, 400, view_checking)
    amount = promo.amount(cart_amount)
    
    if cart_amount < amount:
        return helper_check_promo_code('PROMO_CODE_CANT_BE_USED', request, 400, view_checking)
        
    template = render_to_string(
        'includes/checkout_helpers/promocode_checkout.html',
        {'amount': amount},
        request=request
    )

    data = {
        'message': amount,
        'html': template
    }
    
    if view_checking:
        return data['message'], promo
    else:
       return JsonResponse(data, status=200)


def helper_check_promo_code(message, request, status, view_checking) -> Union[str, JsonResponse]:
    template = render_to_string(
        'includes/checkout_helpers/promocode_fail.html',
        {"message": CUSTOM_MESSAGES[message]},
        request=request,
    )
    data = {
        'message': 'expired',
        'html': template
    }
    return data['message'] if view_checking else JsonResponse(data, status=status)
    
    

class CreateOrderView(View):

    @property
    def cart(self) -> Cart:
        return get_cart(self.request)['cart']

    def get(self, request, *args, **kwargs):
        
        if not self.cart or self.cart.cart_total == 0:
            return redirect('home_page')

        # Getting addresses
        states = State.objects.all().order_by('id')
        cities = Region.objects.filter(state=states.first())

        if request.is_ajax():

            try:
                cities = Region.objects.filter(Q(state_id=int(request.GET['id'])))
                return JsonResponse(data=list(cities.values('name', 'price', 'id')), safe=False)
            except Exception:
                return JsonResponse(data={})

        context = {
            "states": states,
            "regions": cities,
            "cart_items": self.cart.item.all()
        }
        return render(request, 'shop/checkout.html', context)

    @staticmethod
    def _estimate_delivery_coast(data: dict) -> Union[int, float]:
        """Method for estimate delivery coast."""
        delivery_path = None

        state = data.get('state')
        region = data.get('region')
        delivery_path = Region.objects.filter(state__name=state, name=region).first()

        return delivery_path.price if delivery_path else 0

    @staticmethod
    def _adding_order_items(order: Order, items: List[CartItem]) -> None:
        """Method for adding order items."""
        
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                product_image=getattr(item.product, 'main_image'),
                product_price=item.item_price,
                quantity=item.quantity,
                description=item.features
            )
    
    @staticmethod
    def _get_payment_callback(payment_method: str) -> Union[Callable, str]:
        """Method for getting payment making function or some string for skipping the process."""
        
        method_dependencies = {
            Order.PaymentTypeItem.ARCA.value: make_bank_request,
            Order.PaymentTypeItem.IDRAM.value: make_idram_request,
            Order.PaymentTypeItem.CACHE_ON_DELIVERY.value: "cache_on_delivery",
            Order.PaymentTypeItem.IN_MARKET.value: "in_market",
        }
        return method_dependencies[payment_method]
    
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)

        if not form.is_valid():
            return redirect(request.META.get('HTTP_REFERER'))

        order: Order = form.save(commit=False)
        bonus_count = 0
        promosystem = request.POST.get('promosystem')
        bonussystem = request.POST.get('bonussystem')
        
        if promosystem:
            check_promo = check_promo_code(request=request, promo_code=promosystem, view_checking=True)
            
            if isinstance(check_promo, str):
                bonus_count = 0  
            else:
                bonus_count, promo =  check_promo
                promo.decrement_max_usability()
            
            if bonus_count > 0:
                order.used_promo_code = promosystem
            
        if bonussystem:
            bonus_count = 0
        
        
        if order.delivery == Order.DeliveryTypeItem.DELIVERY.value:

            delivery_price = self._estimate_delivery_coast(request.POST)
            order.delivery_price = delivery_price
            order.order_delivery_status = Order.OrderDeliveryStatusItem.IN_PROGRESS.value

        else:

            order.delivery_price = 0
            order.order_delivery_status = Order.OrderDeliveryStatusItem.READY_FOR_TAKING.value

        order.sale_price = bonus_count
        order.cart_total_price = self.cart.cart_total
        order.save()
        
        # Adding order items and then deleting a cart
        self._adding_order_items(order=order, items=self.cart.item.all())
        Cart.objects.filter(id=self.cart.id).delete()
        
        # Getting payment doing function or string about order payment method
        payment_process = self._get_payment_callback(order.payments)
        
        if isinstance(payment_process, Callable):
            # payment_process()
            ...
        

        return redirect('home_page')


class OrderDetailView(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'shop/order_detail.html', {})