# Generated by Django 3.1 on 2022-05-17 20:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0008_auto_20220518_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customresumeforjob',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])]),
        ),
    ]
