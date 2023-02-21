# Generated by Django 3.1 on 2022-03-05 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breadcrumbs', '0002_auto_20220304_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breadcrumbtexts',
            name='location',
            field=models.CharField(choices=[('catalog', 'Տեսականի'), ('sale', 'Ակցիա'), ('new', 'Նորույթ'), ('best_seller', 'Հատուկ առաջարկ'), ('search', 'Որոնում')], max_length=150, unique=True, verbose_name='Ընտրեք էջը'),
        ),
    ]
