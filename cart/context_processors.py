from .models import Cart


def get_cart(request):
    try:
        cart_id = request.session.get('cart_id')

        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            cart = Cart.objects.get(id=cart_id)

        cart = Cart.objects.get(id=cart.id)
        request.session['cart_total'] = cart.item.count()
    except:
        cart = Cart()
        if request.user.is_authenticated:
            cart.user = request.user
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
        request.session['cart_total'] = cart.item.count()
    return {'cart': cart, 'cart_items': cart.item, }
