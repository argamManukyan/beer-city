from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import CreateOrderView



urlpatterns = [
    path('checkout/', csrf_exempt( CreateOrderView.as_view()), name="create_order")
]
