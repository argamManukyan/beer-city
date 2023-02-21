# Generated by Django 3.1 on 2022-03-03 20:51

import canapea.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0037_auto_20220303_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='add_to_ingredients',
            field=models.BooleanField(default=False, verbose_name='Տվյալ բաժնի ապրանքները ավելացնել «Ինգրեդեիենտներում»'),
        ),
        migrations.AlterField(
            model_name='category',
            name='breadcrumb_image',
            field=canapea.utils.CustomLogoField(blank=True, default='defaults/category-banner.jpg', null=True, upload_to='cat-bg-image/', verbose_name='Բաժնի բանների նկար'),
        ),
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=canapea.utils.CustomLogoField(blank=True, default='defaults/category-main.jpg', null=True, upload_to='cat-catalog-image/', verbose_name='Ընդհանուր կատալոգում երևացող նկար'),
        ),
        migrations.AlterField(
            model_name='product',
            name='main_image',
            field=canapea.utils.CustomLogoField(blank=True, default='defaults/product.jpg', upload_to='product-img/'),
        ),
    ]
