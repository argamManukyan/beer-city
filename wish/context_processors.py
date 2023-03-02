from .views import Wish, WishItem

def get_wish(request):
    try:
        wish_id = request.session.get('wish_id')
        if request.user.is_authenticated:
            wish = Wish.objects.filter(user=request.user).first()
        else:
            wish = Wish.objects.get(id=wish_id)

        wish = Wish.objects.get(id=wish.id)
        wish_items = WishItem.objects.filter(wish=wish)

    except:
        wish = Wish()
        if request.user.is_authenticated:
            wish.user = request.user
        wish.save()
        wish_id = wish.id
        request.session['wish_id'] = wish_id
        wish_items = WishItem.objects.filter(wish=wish)

    wish_ids = []
    for i in wish.items.all():
        wish_ids.append(i.product.id)
    return locals()

