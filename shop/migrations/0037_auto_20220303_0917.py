# Generated by Django 3.1 on 2022-03-03 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0036_auto_20220302_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='best_seller',
            field=models.BooleanField(default=False, verbose_name='Բեսթսելեր'),
        ),
    ]
