# Generated by Django 3.1 on 2023-02-25 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0065_auto_20230225_1658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='category',
            name='large_description',
        ),
        migrations.RemoveField(
            model_name='category',
            name='large_description_en',
        ),
        migrations.RemoveField(
            model_name='category',
            name='large_description_hy',
        ),
        migrations.RemoveField(
            model_name='category',
            name='large_description_ru',
        ),
    ]