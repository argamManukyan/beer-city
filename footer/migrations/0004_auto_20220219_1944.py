# Generated by Django 3.1 on 2022-02-19 19:44

import canapea.utils
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('footer', '0003_partners'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankicons',
            name='icon',
            field=canapea.utils.CustomLogoField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='partners',
            name='icon',
            field=canapea.utils.CustomLogoField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='personaldata',
            name='icon',
            field=canapea.utils.CustomLogoField(blank=True, default=1, upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='socialicons',
            name='icon',
            field=canapea.utils.CustomLogoField(upload_to=''),
        ),
    ]
