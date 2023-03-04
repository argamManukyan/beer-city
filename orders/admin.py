from django.contrib import admin

from .models import Order, Bonus, PromoCodes


admin.site.register(Order)
admin.site.register(Bonus)
admin.site.register(PromoCodes)