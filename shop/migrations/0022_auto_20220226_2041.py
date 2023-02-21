# Generated by Django 3.1 on 2022-02-26 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_productingredient_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='productingredient',
            name='qty',
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name='productingredient',
            name='total_price',
            field=models.FloatField(default=0),
        ),
    ]
