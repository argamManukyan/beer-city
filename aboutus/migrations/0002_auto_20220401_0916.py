# Generated by Django 3.1 on 2022-04-01 09:16

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aboutus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutus',
            name='text_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='text_hy',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='text_ru',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
    ]
