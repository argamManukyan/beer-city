# Generated by Django 3.1 on 2022-02-19 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('footer', '0008_auto_20220219_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footer',
            name='is_logged',
            field=models.CharField(blank=True, choices=[('logged', 'Օգտատերեր'), ('guests', 'Հյուրեր')], help_text='Դաշտի հասանելիության տիրույթ', max_length=120, null=True),
        ),
    ]
