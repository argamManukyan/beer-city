# Generated by Django 3.1 on 2023-03-05 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0029_auto_20230304_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='state',
            name='name_hy',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='state',
            name='name_ru',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
