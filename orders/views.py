from typing import Callable, List, Union
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View
from django.utils.translation import ugettext_lazy as _

from cart.context_processors import get_cart
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from orders.service import make_bank_request, make_idram_request
from users.models import Region, State


from .forms import OrderForm


class CreateOrderView(View):

    @property
    def cart(self) -> Cart:
        return get_cart(self.request)['cart']

    def get(self, request, *args, **kwargs):

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
            print(item)
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

        if order.delivery == Order.DeliveryTypeItem.DELIVERY.value:

            delivery_price = self._estimate_delivery_coast(request.POST)
            order.delivery_price = delivery_price
            order.order_delivery_status = Order.OrderDeliveryStatusItem.IN_PROGRESS.value

        else:

            order.delivery_price = 0
            order.order_delivery_status = Order.OrderDeliveryStatusItem.READY_FOR_TAKING.value

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
        

        return JsonResponse({}, status=200)
