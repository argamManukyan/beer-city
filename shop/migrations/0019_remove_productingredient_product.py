# Generated by Django 3.1 on 2022-02-26 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_auto_20220226_2015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productingredient',
            name='product',
        ),
    ]
