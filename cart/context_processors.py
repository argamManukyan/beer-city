from shop.views import get_ip
from .models import Cart


def get_cart(request):
    ip = get_ip(request)
    cart, _ = Cart.objects.get_or_create(ip_address=ip)
    if cart.user is None and request.user.is_authenticated:
        cart.user_id = request.user.id
        cart.save()
    request.session['cart_total'] = cart.item.count()
    return {'cart': cart, 'cart_items': cart.item, }
