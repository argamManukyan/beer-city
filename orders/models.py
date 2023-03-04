from django.db import models
from beercity.utils import CustomModel
from django.utils.translation import ugettext_lazy as _

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
        READY_FOR_TACKING = 4, _('Պատրաստ է վերցնելու') # For taking type
        
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
    
    delivery_type = models.CharField(
        max_length=30, 
        choices=DeliveryTypeItem.choices, 
        verbose_name='Առաքման ձև'
    )
    payment_type = models.CharField(
        max_length=30, 
        choices=PaymentTypeItem.choices, 
        verbose_name='Վճարման եղանակ'
    )
    order_delivery_status = models.IntegerField(
        choices=OrderDeliveryStatusItem.choices,
        verbose_name='Առաքման կարգավիճակ'
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
    
    
    class Meta:
        verbose_name = 'Պատվեր'
        verbose_name_plural = 'Պատվերներ'
    

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