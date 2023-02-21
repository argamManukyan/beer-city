# Generated by Django 3.1 on 2022-02-19 19:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('footer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.FileField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['svg', 'png', 'jpg'])], verbose_name='Լոգո')),
                ('text', models.CharField(max_length=255, verbose_name='Տեքստ')),
                ('my_order', models.PositiveIntegerField(default=0, verbose_name='Դասավորել')),
            ],
            options={
                'verbose_name': 'Ընկերության տվյալ',
                'verbose_name_plural': 'Ընկերության տվյալներ',
                'ordering': ['my_order'],
            },
        ),
        migrations.AlterModelOptions(
            name='bankicons',
            options={'ordering': ['my_order'], 'verbose_name': 'Բանկի լոգո', 'verbose_name_plural': 'Բանկերի լոգոներ'},
        ),
        migrations.AlterModelOptions(
            name='socialicons',
            options={'ordering': ['my_order'], 'verbose_name': 'Սոց ցանցի լոգո', 'verbose_name_plural': 'Սոց ցանցերի լոգոներ'},
        ),
        migrations.RemoveField(
            model_name='footer',
            name='icon',
        ),
        migrations.AlterField(
            model_name='bankicons',
            name='title',
            field=models.CharField(max_length=255, unique=True, verbose_name='Անուն (alt)'),
        ),
        migrations.AlterField(
            model_name='socialicons',
            name='title',
            field=models.CharField(max_length=255, unique=True, verbose_name='Անուն (alt)'),
        ),
    ]
