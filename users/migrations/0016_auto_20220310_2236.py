# Generated by Django 3.1 on 2022-03-10 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20220310_2233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='account_type',
        ),
        migrations.RemoveField(
            model_name='user',
            name='blocked_time',
        ),
        migrations.RemoveField(
            model_name='user',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='sent_verification_code',
        ),
        migrations.RemoveField(
            model_name='user',
            name='verification_code',
        ),
    ]
