# Generated by Django 3.1 on 2022-05-17 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0009_auto_20220518_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='customresumeforjob',
            name='gender',
            field=models.CharField(blank=True, choices=[(1, 'Արական'), (2, 'Իգական'), (3, 'Այլ')], max_length=50, null=True),
        ),
    ]
