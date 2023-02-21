from django.db.models.signals import post_save
from django.dispatch import receiver
from shop.models import Product, Ingredient


@receiver(post_save, sender=Product)
def post_save_ingredients(sender, instance, created, *args, **kwargs):
    if created and instance.category.filter(add_to_ingredients=True).exists():
        Ingredient.objects.create(product=instance,
                                  name=instance.name,
                                  name_hy=instance.name_hy,
                                  name_ru=instance.name_ru,
                                  name_en=instance.name_en,
                                  price=instance.get_price,
                                  is_active=instance.is_active,
                                  main_image=instance.main_image)

    elif not created and instance.category.filter(add_to_ingredients=True).exists():
        ingredient = Ingredient.objects.filter(product=instance)
        if ingredient.exists():
            ingredient.update(name=instance.name,
                              name_hy=instance.name_hy,
                              name_ru=instance.name_ru,
                              name_en=instance.name_en,
                              price=instance.get_price,
                              is_active=instance.is_active,
                              main_image=instance.main_image)
        else:
            Ingredient.objects.create(product=instance,
                                      name=instance.name,
                                      name_hy=instance.name_hy,
                                      name_ru=instance.name_ru,
                                      name_en=instance.name_en,
                                      price=instance.get_price,
                                      is_active=instance.is_active,
                                      main_image=instance.main_image)


def update_category_signal(sender, created, instance, **kwargs):
    category = instance

    if not created:
        if category.add_to_ingredients and \
                not Ingredient.objects.filter(product__category__in=category.id).exists():
            for item in category.product_set.all():
                Ingredient.objects.get_or_create(product=item,
                                                 name=item.name,
                                                 name_hy=item.name_hy,
                                                 name_ru=item.name_ru,
                                                 name_en=item.name_en,
                                                 price=item.get_price,
                                                 is_active=item.is_active,
                                                 main_image=item.main_image)
