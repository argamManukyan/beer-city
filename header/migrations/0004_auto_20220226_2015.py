# Generated by Django 3.1 on 2022-02-26 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('header', '0003_alter_bottomheader_id_alter_topheader_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bottomheader',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='topheader',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
