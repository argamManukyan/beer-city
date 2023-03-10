# Generated by Django 3.1 on 2022-02-21 18:36

import canapea.utils
import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xl_image', canapea.utils.CustomLogoField(upload_to='', verbose_name='Նկար mobile տարբերակի համար')),
                ('lg_image', canapea.utils.CustomLogoField(upload_to='', verbose_name='Նկար desktop տարբերակի համար')),
                ('url', models.URLField(blank=True, null=True, verbose_name='Հղում')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('my_order', models.PositiveIntegerField(default=0, verbose_name='Դասավորել')),
            ],
            options={
                'verbose_name': 'Գլխավոր սլայդերի նկար',
                'verbose_name_plural': 'Գլխավոր սլայդերի նկարներ',
                'ordering': ['my_order'],
            },
        ),
    ]
