# Generated by Django 3.1 on 2022-04-01 09:14

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0024_auto_20220401_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faqmodel',
            name='answer',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=500, verbose_name='Պատասխան'),
        ),
        migrations.AlterField(
            model_name='faqmodel',
            name='answer_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=500, null=True, verbose_name='Պատասխան'),
        ),
        migrations.AlterField(
            model_name='faqmodel',
            name='answer_hy',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=500, null=True, verbose_name='Պատասխան'),
        ),
        migrations.AlterField(
            model_name='faqmodel',
            name='answer_ru',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=500, null=True, verbose_name='Պատասխան'),
        ),
        migrations.AlterField(
            model_name='faqmodel',
            name='question',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=500, verbose_name='Հարց'),
        ),
        migrations.AlterField(
            model_name='faqmodel',
            name='question_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=500, null=True, verbose_name='Հարց'),
        ),
        migrations.AlterField(
            model_name='faqmodel',
            name='question_hy',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=500, null=True, verbose_name='Հարց'),
        ),
        migrations.AlterField(
            model_name='faqmodel',
            name='question_ru',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=500, null=True, verbose_name='Հարց'),
        ),
    ]
