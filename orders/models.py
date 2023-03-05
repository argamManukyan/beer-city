from django.db import models
from beercity.utils import CustomModel
from django.utils.translation import ugettext_lazy as _

from shop.models import ProductFeature

class Order(CustomModel):
    
    class DeliveryTypeItem(models.TextChoices):
        DELIVERY = '1', _('Առաքում')
        TAKING = '2', _('Կվերցնեմ ինքս')
    
    class PaymentTypeItem(models.TextChoices):
        IN_MARKET = '1', _('Կանխիկ տեղում')
        CACHE_ON_DELIVERY = '2', _('Կանխիկ առաքման պահին')
        ARCA = '3', _('Անկանխիկ (ARCA/ VISA/ MASTERCARD)')
        IDRAM = '4', _('Անկանխիկ ("Idram")')
    
    
    class OrderDeliveryStatusItem(models.IntegerChoices):
        IN_PROGRESS = 1, _('Ընթացքի մեջ')
        IN_THE_WAY = 2, _('Ճանապարհին')
        DELIVERED = 3,  _('Առաքված')
        READY_FOR_TAKING = 4, _('Պատրաստ է վերցնելու') # For taking type
        
    class OrderPayingStatusItem(models.IntegerChoices):
        WAITING = 1, _('Սպասման մեջ')
        PAID = 2, _('Վճարված')
        UNPAID = 3, _('Չվճարված')
        REFUNDED = 4, _('Վերադարձված')
               
    # Creator's data
    first_name = models.CharField(max_length=100, verbose_name='Անուն')
    last_name = models.CharField(max_length=100, verbose_name='Ազգանուն')
    phone = models.CharField(max_length=30, verbose_name='Հեռ.')
    email = models.EmailField(verbose_name='Էլ. հասցե')
    
    # Creator's address
    state = models.CharField(max_length=120, blank=True, null=True, verbose_name='Մարզ')
    region = models.CharField(max_length=120, blank=True, null=True, verbose_name='Բնակավայր')
    address = models.TextField(blank=True, null=True, verbose_name='Հասցե')
    notes = models.TextField(blank=True, null=True, verbose_name='Նշումներ')
    
    # Action types
    
    delivery = models.CharField(
        max_length=30, 
        choices=DeliveryTypeItem.choices, 
        verbose_name='Առաքման ձև'
    )
    payments = models.CharField(
        max_length=30, 
        choices=PaymentTypeItem.choices, 
        verbose_name='Վճարման եղանակ'
    )
    order_delivery_status = models.IntegerField(
        choices=OrderDeliveryStatusItem.choices,
        verbose_name='Առաքման կարգավիճակ',
        blank=True, null=True
    )
    order_payment_status = models.IntegerField(
        choices=OrderPayingStatusItem.choices,
        default=OrderPayingStatusItem.WAITING,
        verbose_name='Վճարման կարգավիճակ'
    )
    # Banking part
    
    transaction_id = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name='Բանկային փոխանցման ID'
    )
    transaction_status = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name='Բանկային փոխանցման կարգավիճակ'
    )
    
    # Sales
    
    used_promo_code = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name='Օգտագործված promo կոդ'
    )
    used_bonuses_count = models.FloatField(
        blank=True, 
        null=True, 
        verbose_name='Օգտագործված բոնուսների քանակ'
    )
    
    # Pricing 
    
    cart_total_price = models.FloatField(
        blank=True, 
        null=True, 
        verbose_name='Ապրանքների գումարային արժեք'
    )
    delivery_price = models.FloatField(
        blank=True, 
        null=True, 
        verbose_name='Առաքման գումար'
    )
    order_total_price =  models.FloatField(
        blank=True, 
        null=True, 
        verbose_name='Պատվերի աբողջական արժեք'
    )
    
    def save(self, *args, **kwargs):
        
        delivery_price = self.delivery_price or 0
        cart_total = self.cart_total_price or 0
        self.order_total_price = delivery_price + cart_total

        super(Order, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Պատվեր'
        verbose_name_plural = 'Պատվերներ'
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=250, verbose_name='Ապրանքի անուն')
    product_image = models.ImageField(verbose_name='Նկար')
    product_price = models.FloatField(default=0.0, verbose_name='Գին')
    quantity = models.IntegerField(default=0, verbose_name='Քանակ')
    item_total_price = models.FloatField(default=0, verbose_name='Գումար')
    description = models.CharField(max_length=300, blank=True, null=True, verbose_name='Նկարագրություն')

    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):
        self.item_total_price = self.product_price * self.quantity
        
        if self._state.adding:
            ids = self.description.split(',')

            if ids and self.description:
                item_about = [f'{value.field.title} - {value.value.title}' 
                              for value in ProductFeature.objects.filter(id__in=ids)] if ids else []
                item_about = ' (' + ',  '.join(item_about) + ')' if item_about else ''

                self.product_name = self.product_name + item_about

        super().save(*args, **kwargs)
    

class PromoCodes(CustomModel):
    
    class SaleType(models.TextChoices):
        PERCENT = 1, '%'
        AMOUNT = 2, 'Դրամ'
        
    
    name = models.CharField(max_length=150, unique=True, verbose_name='Կոդ')
    from_date = models.DateTimeField(blank=True, null=True, verbose_name='Գործում է սկսած')
    to_date = models.DateTimeField(blank=True, null=True, verbose_name='Գործում է մինչև')
    max_usability = models.PositiveSmallIntegerField(
        blank=True, 
        null=True, 
        verbose_name='Մաքսիմում կարելի է օգտագործել'
    )
    sale_type = models.CharField(
        choices=SaleType.choices, 
        max_length=30, 
        verbose_name='Զեղչ -ի ձևը'
    )
    percent = models.FloatField(
        verbose_name='Զեղչ -ի չափը'
    )
    
        
    class Meta:
        verbose_name = 'Promo կոդ'
        verbose_name_plural = 'Promo կոդեր'
        
        
    def __str__(self):
        return self.name
        

class Bonus(CustomModel):
    from_price = models.FloatField(verbose_name='Գումարային մինիմալ շեմ')
    to_price = models.FloatField(verbose_name='Գումարային մաքսիմալ շեմ')
    sale_type = models.CharField(
        choices=PromoCodes.SaleType.choices, 
        max_length=30, 
        verbose_name='Զեղչ -ի ձևը'
    )
    percent = models.FloatField(
        verbose_name='Զեղչ -ի չափը'
    )
    
    def __str__(self):
        return f'{self.from_price} - {self.to_price} -> {self.percent} {self.sale_type}'
    
    class Meta:
        verbose_name = 'Բոնուս'
        verbose_name_plural = 'Բոնուսներ'