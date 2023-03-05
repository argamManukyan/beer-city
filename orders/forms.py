from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "state",
            "region",
            "address",
            "notes",
            "delivery",
            "payments",
            "used_promo_code",
            "used_bonuses_count"
        )

    def clean(self):
        cleaned_data = super().clean()
        process_delivery = int(cleaned_data.get('delivery', 0))
        process_payment = int(cleaned_data.get('payments', 0))

        if process_delivery not in list(map(int, Order.DeliveryTypeItem.values)):
            raise forms.ValidationError({"delivery": _("Առաքման տարբերակը սխալ է ընտրված")})

        if process_payment not in list(map(int, Order.PaymentTypeItem.values)):
            raise forms.ValidationError({"payments": ("Վճարման տարբերակը սխալ է ընտրված")})
