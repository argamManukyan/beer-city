# Generated by Django 3.2.7 on 2022-09-20 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactus', '0009_auto_20220702_0813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactusjoinusdata',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Ստեղծվել է'),
        ),
        migrations.AlterField(
            model_name='contactusjoinusdata',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Թարմացվել է'),
        ),
        migrations.AlterField(
            model_name='contactuspage',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Ստեղծվել է'),
        ),
        migrations.AlterField(
            model_name='contactuspage',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Թարմացվել է'),
        ),
        migrations.AlterField(
            model_name='contactusrequest',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Ստեղծվել է'),
        ),
        migrations.AlterField(
            model_name='contactusrequest',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Թարմացվել է'),
        ),
        migrations.AlterField(
            model_name='followuscontactus',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Ստեղծվել է'),
        ),
        migrations.AlterField(
            model_name='followuscontactus',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Թարմացվել է'),
        ),
    ]
