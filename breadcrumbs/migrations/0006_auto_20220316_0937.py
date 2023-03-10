# Generated by Django 3.1 on 2022-03-16 09:37

import canapea.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breadcrumbs', '0005_auto_20220315_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breadcrumbtexts',
            name='breadcrumbs_image',
            field=canapea.utils.CustomLogoField(blank=True, null=True, upload_to='', verbose_name='Breadcrumb -ի Նկար'),
        ),
        migrations.AlterField(
            model_name='breadcrumbtexts',
            name='location',
            field=models.CharField(choices=[('catalog', 'Տեսականի'), ('sale', 'Ակցիա'), ('new', 'Նորույթ'), ('best_seller', 'Բեսթսելլեր'), ('special_offer', 'Հատուկ առաջարկ'), ('search', 'Որոնում')], max_length=150, unique=True, verbose_name='Ընտրեք էջը'),
        ),
        migrations.AlterField(
            model_name='breadcrumbtexts',
            name='page_title',
            field=models.CharField(blank=True, max_length=255, verbose_name='Էջի վերնագիր'),
        ),
        migrations.AlterField(
            model_name='breadcrumbtexts',
            name='page_title_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Էջի վերնագիր'),
        ),
        migrations.AlterField(
            model_name='breadcrumbtexts',
            name='page_title_hy',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Էջի վերնագիր'),
        ),
        migrations.AlterField(
            model_name='breadcrumbtexts',
            name='page_title_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Էջի վերնագիր'),
        ),
    ]
