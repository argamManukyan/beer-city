# Generated by Django 3.2 on 2022-06-02 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactus', '0002_bookings_workinghours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='date_of_book',
            field=models.DateField(verbose_name='Ամրագրման օրը'),
        ),
    ]
