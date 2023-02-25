import time
from datetime import timedelta
from colorfield.fields import ColorField
from auditlog.registry import auditlog
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone

from beercity.utils import *
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey


class SliderPhoneImage(models.Model):
    image = models.FileField(upload_to='slider_image', verbose_name="Գլխավոր էջի սլայդերի ֆոնային նկար")
    
    def __str__(self):
        return "Գլխավոր էջի սլայդերի ֆոնային նկար"
    
    class Meta:
        verbose_name = "Գլխավոր էջի սլայդերի ֆոնային նկար"
        verbose_name_plural = "Գլխավոր էջի սլայդերի ֆոնային նկար"
    

class Slider(models.Model):
    xl_image = CustomLogoField(verbose_name='Նկար mobile տարբերակի համար')
    lg_image = CustomLogoField(verbose_name='Նկար desktop տարբերակի համար')
    url = models.URLField(verbose_name='Հղում', blank=True, null=True)
    text = RichTextUploadingField(blank=True, null=True)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Գլխավոր սլայդերի նկար'
        verbose_name_plural = 'Գլխավոր սլայդերի նկարներ'

    def __str__(self):
        return str(self.pk)


class BonusDays(models.Model):
    """ Table for any sale-days, for example black friday """
    title = models.CharField(max_length=255, unique=True, verbose_name='Անուն')
    is_active = models.BooleanField(default=True, verbose_name='Հասանելի է')
    active_from = models.DateTimeField(verbose_name='Զեղչի սկիզբ')
    active_to = models.DateTimeField(verbose_name='Զեղչի ավարտ')
    icon = CustomLogoField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Բոնուսային օր'
        verbose_name_plural = 'Բոնուսային օրեր'


class Category(MPTTModel, CustomMetaModel):
    name = models.CharField(max_length=255, verbose_name='Բաժնի անուն')
    slug = models.SlugField(unique=True, null=True, blank=True, verbose_name='Հղում')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children', verbose_name='Հայրական բաժին')

    icon = CustomLogoField(verbose_name='Ընդհանուր կատալոգում երևացող նկար', blank=True, null=True,
                           upload_to='cat-catalog-image/', default='defaults/category-main.jpg')
    logo = CustomLogoField(verbose_name='Գլխավոր էջի կատեգորիայի նկար', blank=True,
                           null=True, upload_to='cat-img/',)
    breadcrumb_image = CustomLogoField(verbose_name='Բաժնի բանների նկար', default='defaults/category-banner.jpg',
                                       blank=True, null=True, upload_to='cat-bg-image/')

    short_description = models.TextField(blank=True, null=True, verbose_name='Հակիրճ նկարագրություն')
    large_description = RichTextUploadingField(blank=True, null=True, verbose_name='Ամբողջական նկարագրություն')
    color = ColorField(default='#FF0000', blank=True, null=True, verbose_name='Background -ի գույն',
                       help_text='Ընտրված գույնը երևում է header -ում, որպես տվյալ բաժնի ֆոնի գույն')

    show_in_header = models.BooleanField(default=False, verbose_name='Ցուցադրել գլխավոր էջում')
    is_active = models.BooleanField(default=True, verbose_name='Ակտիվ կարգավիճակ')
    # Trigger for example macaroons
    show_category_all_items = models.BooleanField(default=False, 
                                                  verbose_name='Ցուցադրել բաժնի բոլոր ապրանքները ապրանքի էջում')

    # Trigger for add products to the ingredients list
    add_to_ingredients = models.BooleanField(default=False, verbose_name='Տվյալ բաժնի ապրանքները ավելացնել «Ինգրեդեիենտներում»')

    class Meta:
        verbose_name = 'Բաժին'
        verbose_name_plural = 'Բաժիններ'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_generator(title=self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={"slug": self.slug})

    def __str__(self):
        title_list = [self.name]
        parent = self.parent

        while parent is not None:
            title_list.append(parent.name)
            parent = parent.parent

        return '-->'.join(title_list[::-1]) or ''

auditlog.register(Category)


class CategoryBonuses(models.Model):
    category = models.OneToOneField(
        Category,
        on_delete=models.CASCADE,
        related_name='bonus_days',
        verbose_name="Բաժնի անուն"
    )
    bonus = models.ForeignKey(BonusDays, on_delete=models.PROTECT, verbose_name="Բոնուսի անվանում")
    percent = models.FloatField(default=0.0, verbose_name="Զեղչի տոկոս")

    def __str__(self):
        return f"{self.category.name}: {self.percent}%"

    class Meta:
        verbose_name = 'Բաժնի բոնուսային օր'
        verbose_name_plural = 'Բաժնի բոնուսային օրեր'


class FilterField(models.Model):
    """ Filter field table """
    FIELD_TYPES = [
        ('radio', 'Radio'),
        ('select', 'Dropdown'),
    ]

    category = models.ManyToManyField(Category, verbose_name='Բաժին', )
    filter_key = models.CharField(max_length=150, unique=True, blank=True, editable=False)
    title = models.CharField(verbose_name='Դաշտի անուն', max_length=255, unique=True)
    show_in_filters = models.BooleanField(verbose_name='Ցուցադրել ֆիլտրերում', default=False)
    is_main = models.BooleanField(verbose_name='Հիմնական դաշտ', default=False)
    field_type = models.TextField(choices=FIELD_TYPES, blank=True, null=True, max_length=50, verbose_name='Դաշտի տիպը')
    help_field_title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Օգնող դաշտի վերնագիր')
    help_field_content = RichTextUploadingField(blank=True, null=True, verbose_name='Օգնող դաշտի տեքստ')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.filter_key:
            self.filter_key = unidecode(self.title.replace(' ', '_'))

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ֆիլտրացման դաշտ'
        verbose_name_plural = 'Ֆիլըտրացման դաշտեր'


class FilterValue(models.Model):
    """ Filter value table """

    title = models.CharField(verbose_name='Ֆիլտրացման արժեք', max_length=255, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ֆիլտրվող արժեքներ'
        verbose_name_plural = 'Ֆիլտրվեղ արժեքներ'

    def save(self, *args, **kwargs):
        self.title = smart_strip(self.title)
        super().save(*args, **kwargs)


class Color(CustomModel):
    """ Color table """
    title = models.CharField(verbose_name='Գույնի անուն', max_length=255)
    color_code = ColorField(default="#fff", blank=True, null=True, verbose_name='Գույնի կոդ')
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Գույն'
        verbose_name_plural = 'Գույներ'


class Brand(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name='Անուն')
    slug = models.SlugField(verbose_name='Հղում', blank=True, null=True, unique=True)
    icon = models.FileField(verbose_name='Լոգո', blank=True, null=True)
    shipper_email = models.EmailField(verbose_name='Էլ. փոստ', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Բրենդ'
        verbose_name_plural = 'Բրենդներ'
        
    
class Product(CustomMetaModel):
    category = models.ManyToManyField(Category, verbose_name='Ընտրել բաժինը / բաժինները')
    brand = models.ForeignKey(Brand, verbose_name='Բրենդ', 
                              blank=True, 
                              null=True,
                              on_delete=models.CASCADE
                              )
    name = models.CharField(max_length=255, verbose_name='Ապրանքի անվանում')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Հղում', blank=True)
    large_description = RichTextUploadingField(blank=True, null=True, verbose_name='Ամբողջական նկարագրություն')
    price = models.IntegerField(default=0, verbose_name='Ապրանքի գին')
    sale = models.IntegerField(default=0, verbose_name='Ապրանքի զեղչված գին')
    is_active = models.BooleanField(default=True, verbose_name='Առկա է')
    min_qty = models.PositiveSmallIntegerField(default=1, verbose_name='Թույլատրելի մինիմալ քանակություն')
    max_qty = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Թույլատրելի մաքսիմալ քանակություն')
    main_image = CustomLogoField(upload_to='product-img/', blank=True, default='defaults/product.jpg')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    finally_price = models.PositiveIntegerField(verbose_name='', default=0, editable=False)
    mark_as_bestseller_count = models.PositiveSmallIntegerField(default=1,
                                                                verbose_name='Վաճառքի քանակ, որից հետո ապրանքը'
                                                                             ' կհամարվի best seller ')
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')
    special_offer = models.BooleanField(default=False, verbose_name="Հատուկ առաջարկ")
    # TODO: after sold selected count of this product mark as best seller
    best_seller = models.BooleanField(default=False, verbose_name="Բեսթսելեր")
    # TODO: Implement logic for filter price
    bonus_day_not_working = models.BooleanField(default=False,
                                                verbose_name='Անտեսել բաժնի / բաժինների վրա տարածվող զեղչը')
    product_code = models.CharField(max_length=255,
                                    blank=True,
                                    null=True, 
                                    unique=True,
                                    verbose_name='Ապրանքի կոդ')
    product_custom_id = models.CharField(max_length=255, 
                                    blank=True, 
                                    null=True, 
                                    unique=True,
                                    verbose_name='Ապրանքի ID'
                                    )
    sold_count = models.PositiveIntegerField(default=0, verbose_name='Վաճառված քանակություն')
    buy_with_this_item = models.ManyToManyField('self', blank=True, related_name='buywiththis',
                                                verbose_name='Այս ապրանքի հետ գնում են նաև')
    show_minus_and_plus = models.BooleanField(default=True, verbose_name="Ցուցադրել «+» և «-» նշանները ապրանքի բլոկում")
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.product_custom_id:
            self.product_custom_id = f'BC0{int(time.time())}'
        
        self.finally_price = self.sale if self.sale > 1 else self.price
        if not self.slug:
            self.slug = slug_generator(title=self.name)

        super().save(*args, **kwargs)

    @property
    def is_new(self):
        """ Check is it product added not more than 15 days """
        return self.created_at >= timezone.now() - timedelta(days=15)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    @property
    def get_sale_percent(self):
        """ Calculating sale percent """
        if self.sale < 1:
            return 0
        else:
            return float('{:.1f}'.format((self.price - self.sale) / (self.price / 100)))

    @property
    def get_price(self):
        return self.sale if self.sale > 0 else self.price

    class Meta:
        ordering = ['-my_order']
        verbose_name = 'Ապրանք'
        verbose_name_plural = 'Ապրանքներ'


class Rating(CustomModel):
    """ Rating values model """
    value = models.IntegerField(default=1, unique=True)

    def __str__(self):
        return str(self.value)


class RatingProduct(CustomModel):
    """ Rating of products model """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.SET_NULL, null=True, blank=True)
    ip = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.product.name} - {self.rating}'


class Ingredient(models.Model):
    """ Ingredient table for occasions """

    product = models.OneToOneField("Product", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name='Ապրանքի անվանում')
    price = models.IntegerField(default=0, verbose_name='Ապրանքի գին')
    is_active = models.BooleanField(default=True, verbose_name='Առկա է')
    main_image = CustomLogoField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ինգրեդիենտ'
        verbose_name_plural = 'Ինգրեդիենտներ'


class ProductImage(CustomModel):
    """ Product images table """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = CustomLogoField(verbose_name='product-img/')
    my_order = models.PositiveIntegerField(default=0, verbose_name='Դասավորել')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Ապրանքի նկար'
        verbose_name_plural = 'Ապրանքի նկարներ'
        ordering = ['my_order']


class ProductFeature(CustomModel):
    """ Product feature table """

    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='Ապրանքի անուն',
                                )
    field = models.ForeignKey(FilterField, verbose_name='Դաշտ', on_delete=models.SET_NULL, null=True)
    value = models.ForeignKey(FilterValue, verbose_name='Դաշտի արժեք', on_delete=models.SET_NULL, null=True)
    measure_unit = models.ForeignKey(
        'UnitMeasurement',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Չափման միավոր'
    )
    price = models.IntegerField(verbose_name='Գին', default=0)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')
    is_active = models.BooleanField(default=True, verbose_name='Ակտիվ է')
    show_on_product_block = models.BooleanField(default=False, verbose_name='Ցուցադրել ապրանքի բլոկում')

    def __str__(self):
        return f'{self.product.name} - {self.value}'

    class Meta:
        verbose_name = 'Ապրանքի չափորոշիչ'
        verbose_name_plural = 'Ապրանքի չափորոշիչներ'
        unique_together = ['product', 'field', 'value']
        ordering = ['my_order']


class UnitMeasurement(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.title = smart_strip(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductIngredient(models.Model):
    """ for canape """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ingredients')
    ingredients = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='product_ingredients')
    qty = models.PositiveIntegerField(default=1)
    total_price = models.FloatField(default=0)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')
    infinite = models.BooleanField(default=False, verbose_name='Անսահմանափակ')
    measure_unit = models.ForeignKey(
                                UnitMeasurement,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                verbose_name='Չափման միավոր'
                            )

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if self.total_price == 0:
            self.total_price = self.qty * self.ingredients.price

        super().save(*args, **kwargs)

    def clean(self):
        if self.pk and self.ingredients.product and self.product.pk == self.ingredients.product_id:
            raise ValidationError({"ingredients": "Ապրանքը չի կարող լինել ինքն իրեն որպես ինգրեդիենտ"})

    class Meta:
        verbose_name = 'Ապրանքի Ինգրեդիենտ'
        verbose_name_plural = 'Ապրանքի Ինգրեդիենտներ'
        unique_together = ['product', 'ingredients']
        ordering = ['my_order']


class HomepageBanners(models.Model):
    image = CustomLogoField()
    url = models.URLField(verbose_name='Հղում')
    name = models.CharField(max_length=255, verbose_name='Վերնագիր')
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')
    description = RichTextUploadingField(blank=True, verbose_name='Տեքստ')
    color = ColorField(verbose_name='Գույն', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Գլխավոր էջի բաններ'
        verbose_name_plural = 'Գլխավոր էջի բաններներ'
        ordering = ['my_order']

    def __str__(self):
        return self.name


class HomePageSEOText(CustomModel):
    text = RichTextUploadingField()

    class Meta:
        verbose_name = 'Գլխավոր էջի SEO -ի տեքստ'
        verbose_name_plural = 'Գլխավոր էջի SEO -ի տեքստ'


class Bullets(models.Model):

    title = models.CharField(max_length=255, verbose_name='Վերնագիր')
    icon = CustomLogoField()
    text = models.TextField(blank=True, null=True, verbose_name='Նկարագիր')
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Առավելություն'
        verbose_name_plural = 'Մեր առավելություններ'
        ordering = ['my_order']


class Subscriptions(CustomModel):
    email = models.EmailField()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Բաժանորդագրություն'
        verbose_name_plural = 'Բաժանորդագրություններ'

