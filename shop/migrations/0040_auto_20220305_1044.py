# Generated by Django 3.1 on 2022-03-05 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0039_auto_20220305_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='buy_with_this_item',
            field=models.ManyToManyField(blank=True, related_name='_product_buy_with_this_item_+', to='shop.Product', verbose_name='Այս ապրանքի հետ գնում են նաև'),
        ),
    ]
