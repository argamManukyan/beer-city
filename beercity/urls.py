from django.contrib import admin
from django.conf.urls.static import static, settings
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.i18n import i18n_patterns

from cart.views import AddToCartView, ChangeQuantityBasketView, RemoveFromBAsketView
from flatpages.views import like_post
from shop.views import create_rating, setcurrency, ajaxSearch, change_qty
from users.views import check_otp, resend_otp_code
from wish.views import add_to_wish

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('currencies/', include('currencies.urls')),
    path('setcurrency/', csrf_exempt(setcurrency), name='setcurrency'),
    path('add-rating/', create_rating, name='create_rating'),
    path('add_to_wish/', add_to_wish, name='add_to_wish'),
    path('rosetta/', include('rosetta.urls')),
    path('result/', ajaxSearch, name='ajaxsearch'),

    # TODO: remove from u-patterns and set to multilang

    path('add-to-cart/', csrf_exempt(AddToCartView.as_view())),
    path('change-qty/', csrf_exempt(ChangeQuantityBasketView.as_view())),
    path('remove-basket/', csrf_exempt(RemoveFromBAsketView.as_view())),
    path('check-otp/', csrf_exempt(check_otp), name='check_otp'),
    path('like/', csrf_exempt(like_post), name='like_post'),
    path('index/', include('shop.urls')),
    path('index/', include('wish.urls')),
    path('index/', include('contactus.urls')),
    path('index/', include('cart.urls')),
    path('index/', include('users.urls', namespace='users')),
    path('index/', include('flatpages.urls')),
    path('change-qty/<pk>/', change_qty, name='change_qty')

]
#
urlpatterns += i18n_patterns(
    path('index/', include('shop.urls')),
    path('index/', include('contactus.urls')),
    path('index/', include('wish.urls')),
    path('index/', include('cart.urls')),
    path('index/', include('users.urls', namespace='users')),
    path('index/', include('flatpages.urls')),
    prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
