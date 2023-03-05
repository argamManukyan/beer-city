# Generated by Django 3.1 on 2023-03-04 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ստեղծման օր')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ձևափոխման օր')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('state', models.CharField(blank=True, max_length=120, null=True)),
                ('region', models.CharField(blank=True, max_length=120, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('delivery_type', models.CharField(choices=[('1', 'Առաքում'), ('2', 'Կվերցնեմ ինքս')], max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]