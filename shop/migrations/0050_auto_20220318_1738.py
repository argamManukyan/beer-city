# Generated by Django 3.1 on 2022-03-18 17:38

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0049_auto_20220317_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageSEOText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ստեղծման օր')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ձևափոխման օր')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField()),
            ],
            options={
                'verbose_name': 'Գլխավոր էջի SEO -ի տեքստ',
                'verbose_name_plural': 'Գլխավոր էջի SEO -ի տեքստ',
            },
        ),
        migrations.RemoveField(
            model_name='productingredient',
            name='measure_unit',
        ),
        migrations.DeleteModel(
            name='UnitMeasurement',
        ),
    ]
