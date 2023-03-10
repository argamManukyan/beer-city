# Generated by Django 3.1 on 2022-03-18 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0050_auto_20220318_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitMeasurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='productingredient',
            name='measure_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.unitmeasurement', verbose_name='Չափման միավոր'),
        ),
    ]
