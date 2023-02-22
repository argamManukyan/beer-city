# Generated by Django 4.0.2 on 2022-02-24 19:11

import beercity.utils
import ckeditor_uploader.fields
import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_category_show_bottom_alter_category_breadcrumb_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilterValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Ֆիլտրացման արժեք')),
            ],
            options={
                'verbose_name': 'Ֆիլտրվող արժեքներ',
                'verbose_name_plural': 'Ֆիլտրվեղ արժեքներ',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='add_to_ingredients',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='category',
            name='show_category_all_items',
            field=models.BooleanField(default=False, verbose_name='Ցուցադրել բաժնի բոլոր ապրանքները ապրանքի էջում'),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('meta_title', models.CharField(blank=True, max_length=160)),
                ('meta_description', models.TextField(blank=True, max_length=300)),
                ('name', models.CharField(max_length=255, verbose_name='Ապրանքի անվանում')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Հղում')),
                ('short_description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Հակիրճ նկարագրություն')),
                ('large_description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Ամբողջական նկարագրություն')),
                ('price', models.IntegerField(default=0, verbose_name='Ապրանքի գին')),
                ('sale', models.IntegerField(default=0, verbose_name='Ապրանքի զեղչված գին')),
                ('is_active', models.BooleanField(default=True, verbose_name='Հասանելի է')),
                ('min_qty', models.PositiveSmallIntegerField(default=1, verbose_name='Թույլատրելի մինիմալ քանակություն')),
                ('main_image', beercity.utils.CustomLogoField(upload_to='')),
                ('color', colorfield.fields.ColorField(blank=True, default='#fff', image_field=None, max_length=18, null=True, samples=None, verbose_name='Գույն')),
                ('mark_as_bestseller_count', models.PositiveSmallIntegerField(default=1, verbose_name='Վաճառքի քանակ, որից հետո ապրանքը կհամարվի best seller ')),
                ('category', models.ManyToManyField(to='shop.Category', verbose_name='Ընտրել Բաժինը/բաժինները')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FilterField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter_key', models.CharField(blank=True, editable=False, max_length=150, unique=True)),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Դաշտի անուն')),
                ('show_in_filters', models.BooleanField(default=False, verbose_name='Ցուցադրել ֆիլտրերում')),
                ('is_main', models.BooleanField(default=False, verbose_name='Հիմնական դաշտ')),
                ('field_type', models.TextField(blank=True, choices=[('radio', 'Radio'), ('select', 'Dropdown')], max_length=50, null=True, verbose_name='Դաշտի տիպը')),
                ('help_field_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Օգնող դաշտի վերնագիր')),
                ('help_field_content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Օգնող դաշտի տեքստ')),
                ('category', models.ManyToManyField(to='shop.Category', verbose_name='Բաժին')),
            ],
            options={
                'verbose_name': 'Ֆիլտրացման դաշտ',
                'verbose_name_plural': 'Ֆիլըտրացման դաշտեր',
            },
        ),
    ]
