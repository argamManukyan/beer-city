# Generated by Django 3.1 on 2022-02-17 21:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankIcons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, null=True, verbose_name='Հղում')),
                ('icon', models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['svg', 'png', 'jpg'])], verbose_name='Լոգո')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Անուն')),
                ('my_order', models.PositiveIntegerField(default=0, verbose_name='Դասավորել')),
            ],
            options={
                'ordering': ['my_order'],
            },
        ),
        migrations.CreateModel(
            name='Footer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Դաշտի անուն')),
                ('url', models.URLField(verbose_name='Հղում')),
                ('icon', models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['svg', 'png', 'jpg'])], verbose_name='Լոգո')),
                ('my_order', models.PositiveIntegerField(default=0, verbose_name='Դասավորել')),
            ],
            options={
                'ordering': ['my_order'],
            },
        ),
        migrations.CreateModel(
            name='SocialIcons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='Հղում')),
                ('icon', models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['svg', 'png', 'jpg'])], verbose_name='Լոգո')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Անուն')),
                ('my_order', models.PositiveIntegerField(default=0, verbose_name='Դասավորել')),
            ],
            options={
                'ordering': ['my_order'],
            },
        ),
    ]
