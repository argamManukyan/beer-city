# Generated by Django 3.1 on 2023-03-02 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_auto_20230302_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='features',
        ),
    ]