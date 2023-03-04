from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render
from django.views import View

from orders.models import Order
from users.models import Region, State

from .forms import OrderForm


class CreateOrderView(View):
    
    def get(self, request, *args, **kwargs):
        
        cart_items = []
        
        states = State.objects.all().order_by('id')
        cities = Region.objects.filter(state=states.first())

        if request.is_ajax():

            try:
                cities = Region.objects.filter(Q(state_id=int(request.GET['id'])))
                return JsonResponse(data=list(cities.values('name', 'price', 'id')), safe=False)
            except Exception:
                return JsonResponse(data={})

        return render(request, 'shop/checkout.html', {"cart_items": cart_items})
    
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        
        state = form.cleaned_data.get('state')
        region = form.cleaned_data.get('region')
        
        if state or region:
            ...            
        
        if form.is_valid():
            form: Order = form.save(commit=False)
            