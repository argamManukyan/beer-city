# Generated by Django 3.1 on 2022-03-08 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20220308_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verification_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
