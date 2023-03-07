from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import CreateOrderView, OrderDetailView



urlpatterns = [
    path('checkout/', csrf_exempt(CreateOrderView.as_view()), name="create_order"),
    path('order-details/<int:pk>/', OrderDetailView.as_view(), name="order_details"),
]
