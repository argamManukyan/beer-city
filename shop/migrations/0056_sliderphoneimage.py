# Generated by Django 3.1 on 2023-02-22 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0055_product_show_minus_and_plus'),
    ]

    operations = [
        migrations.CreateModel(
            name='SliderPhoneImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='slider_image', verbose_name='Գլխավոր էջի սլայդերի ֆոնային նկար')),
            ],
        ),
    ]
