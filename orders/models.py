from django.db import models
from django.forms import ValidationError
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
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
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
    sale_price = models.FloatField(
        blank=True, 
        null=True, 
        verbose_name='Պատվերից զեղչվել է'
    )
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
        sale_price = self.sale_price or 0
        self.order_total_price = delivery_price + cart_total - sale_price
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
        verbose_name='Տիպը'
    )
    percent = models.FloatField(
        verbose_name='Զեղչ -ի չափը'
    )
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Promo կոդ'
        verbose_name_plural = 'Promo կոդեր'
        
    def save(self, *args, **kwargs):
        if isinstance(self.max_usability, int) and self.max_usability == 0:
            self.is_active = 0
        super().save(*args, **kwargs)
    
    def amount(self, cart_amount):
        if self.sale_type == self.SaleType.AMOUNT:
            return self.percent
        return self.percent * cart_amount / 100
    
    def decrement_max_usability(self):
        if self.max_usability:
            self.max_usability -= 1
            self.save()
    
    def clean(self) -> None:
        if self.percent and self.percent > 100 and self.sale_type and self.sale_type == self.SaleType.PERCENT:
            raise ValidationError({"percent": 'Մաքսիմում թույլատրելի արժեքը՝ 100'})
        
        if self.percent and self.percent < 0 and self.sale_type and self.sale_type == self.SaleType.PERCENT:
            raise ValidationError({"percent": 'Մինիմում թույլատրելի արժեքը՝ 0'})
         
    def __str__(self):
        return self.name
        

class Bonus(CustomModel):
    from_price = models.FloatField(verbose_name='Գումարային մինիմալ շեմ')
    to_price = models.FloatField(verbose_name='Գումարային մաքսիմալ շեմ')
    sale_type = models.CharField(
        choices=PromoCodes.SaleType.choices, 
        max_length=30, 
        verbose_name='Տիպը'
    )
    percent = models.FloatField(
        verbose_name='Զեղչ -ի չափը'
    )
    
    def __str__(self):
        return f'{self.from_price} - {self.to_price} -> {self.percent} {self.get_sale_type_display()}'
    
    def amount(self, cart_amount):
        if self.sale_type == PromoCodes.SaleType.AMOUNT:
            return self.percent
        return self.percent * cart_amount / 100
    
    class Meta:
        verbose_name = 'Բոնուս'
        verbose_name_plural = 'Բոնուսներ'
        

class ApplicationConstants(models.Model):
    
    bonus_to_amd = models.FloatField(default=1, verbose_name='1 բոնուսային միավորը AMD -ի տեսքով')
    promo_percent_type = models.CharField(
        choices=PromoCodes.SaleType.choices, max_length=120, verbose_name='Տիպը'
    )
    promo_sale = models.FloatField(default=1, verbose_name='Տրամադրվող զեղչի չափ')
    
    def clean(self) -> None:
        if (
            self.promo_sale
            and self.promo_sale > 100
            and self.promo_sale == PromoCodes.SaleType.PERCENT
        ):
            raise ValidationError({"percent": 'Մաքսիմում թույլատրելի արժեքը՝ 100'})

        if (
            self.promo_sale 
            and self.promo_sale < 0 
            and self.promo_percent_type 
            and self.promo_percent_type == PromoCodes.SaleType.PERCENT
        ):
            raise ValidationError({"percent": 'Մինիմում թույլատրելի արժեքը՝ 0'})