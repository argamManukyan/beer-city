from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Order, Bonus, PromoCodes, OrderItem


class OrderItemAdmin(admin.TabularInline):
    readonly_fields = ['product_name', 'product_price', 'quantity', 'item_total_price']
    exclude = ['description', 'product', 'product_image']
    
    def get_image(self, obj: OrderItem):
        if obj.product_image:
            return mark_safe(f'<img src="{obj.product_image.url}" width="100px" height="100px" />')
        return mark_safe(
            '<img src="/media/defaults/product.jpg" width="120px" height="120px" />'
        )
    
    get_image.short_description = 'Նկար'
    
    readonly_fields.insert(0, 'get_image')
    
    model = OrderItem
    extra = 0
    

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemAdmin]
    list_display = [i.name for i in Order._meta.fields if i.name not in ['created_at', 'updated_at']]
    list_display.extend(['created_at', 'updated_at'])
    
admin.site.register(Order, OrderAdmin)
admin.site.register(Bonus)
admin.site.register(PromoCodes)