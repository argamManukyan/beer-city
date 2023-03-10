# Generated by Django 4.0.2 on 2022-02-24 20:05

import canapea.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_product_color'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='color',
            options={'ordering': ['my_order'], 'verbose_name': 'Գույն', 'verbose_name_plural': 'Գույներ'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['my_order'], 'verbose_name': 'Ապրանք', 'verbose_name_plural': 'Ապրանքներ'},
        ),
        migrations.AddField(
            model_name='color',
            name='my_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Դասավորել'),
        ),
        migrations.AddField(
            model_name='product',
            name='my_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Դասավորել'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', canapea.utils.CustomLogoField(upload_to='')),
                ('my_order', models.PositiveIntegerField(default=0, verbose_name='Դասավորել')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
            options={
                'verbose_name': 'Ապրանքի նկար',
                'verbose_name_plural': 'Ապրանքի նկարներ',
                'ordering': ['my_order'],
            },
        ),
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('price', models.IntegerField(default=0, verbose_name='Գին')),
                ('my_order', models.PositiveIntegerField(default=0, verbose_name='Դասավորել')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ակտիվ է')),
                ('show_on_product_block', models.BooleanField(default=True, verbose_name='Ցուցադրել ապրանքի բլոկում')),
                ('field', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.filterfield', verbose_name='Դաշտ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='shop.product', verbose_name='Ապրանքի անուն')),
                ('value', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.filtervalue', verbose_name='Դաշտի արժեք')),
            ],
            options={
                'verbose_name': 'Ապրանքի չափորոշիչ',
                'verbose_name_plural': 'Ապրանքի չափորոշիչներ',
                'ordering': ['my_order'],
                'unique_together': {('product', 'field', 'value')},
            },
        ),
    ]
