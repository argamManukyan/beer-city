# Generated by Django 3.1 on 2023-02-25 16:04

import beercity.utils
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0070_auto_20230225_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='social_image',
            field=beercity.utils.CustomLogoField(blank=True, null=True, upload_to='cat-social-image/', verbose_name='Social Media նկար'),
        ),
    ]
