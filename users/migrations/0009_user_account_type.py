# Generated by Django 3.1 on 2022-03-07 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_user_blocked_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='account_type',
            field=models.CharField(choices=[('personal', 'Ֆիզիկական'), ('company', 'Իրավաբանական')], default=1, max_length=80),
            preserve_default=False,
        ),
    ]
