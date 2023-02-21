# Generated by Django 3.1 on 2022-02-28 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0028_auto_20220228_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='meta_description_en',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_description_hy',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_description_ru',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_title_en',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_title_hy',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_title_ru',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_description_en',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_description_hy',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_description_ru',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_title_en',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_title_hy',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_title_ru',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
    ]
