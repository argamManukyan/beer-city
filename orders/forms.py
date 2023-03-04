from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = (
            "first_name", "last_name",
            "email", "phone",
            "state", "region", "address",
            "notes", "delivery_type", 
            "payment_type",
            "used_promo_code",
            "used_bonuses_count"
        )