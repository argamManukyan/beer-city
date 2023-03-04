# Generated by Django 3.1 on 2023-03-04 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_payment_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ստեղծման օր')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ձևափոխման օր')),
                ('from_price', models.FloatField()),
                ('to_price', models.FloatField()),
                ('percent', models.FloatField(blank=True, null=True)),
                ('sale_type', models.CharField(choices=[('1', '%'), ('2', 'Դրամ')], max_length=30)),
            ],
            options={
                'verbose_name': 'Բոնուս',
                'verbose_name_plural': 'Բոնուսներ',
            },
        ),
        migrations.CreateModel(
            name='PromoCodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ստեղծման օր')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ձևափոխման օր')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('from_date', models.DateTimeField(blank=True, null=True)),
                ('to_date', models.DateTimeField(blank=True, null=True)),
                ('max_usability', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('percent', models.FloatField(blank=True, null=True)),
                ('sale_type', models.CharField(choices=[('1', '%'), ('2', 'Դրամ')], max_length=30)),
            ],
            options={
                'verbose_name': 'Promo կոդ',
                'verbose_name_plural': 'Promo կոդեր',
            },
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Պատվեր', 'verbose_name_plural': 'Պատվերներ'},
        ),
        migrations.AddField(
            model_name='order',
            name='cart_total_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_total_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='transaction_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='used_bonuses_count',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='used_promo_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
