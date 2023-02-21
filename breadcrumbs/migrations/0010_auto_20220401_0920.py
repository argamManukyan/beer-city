# Generated by Django 3.1 on 2022-04-01 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breadcrumbs', '0009_auto_20220331_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breadcrumbtexts',
            name='location',
            field=models.CharField(choices=[('catalog', 'Տեսականի'), ('sale', 'Ակցիա'), ('new', 'Նորույթ'), ('best_seller', 'Բեսթսելլեր'), ('special_offer', 'Հատուկ առաջարկ'), ('search', 'Որոնում'), ('blog', 'Բլոգ'), ('gallery', 'Տեսադարան'), ('contacts', 'Կապ'), ('abouts', 'Մեր մասին')], max_length=150, unique=True, verbose_name='Ընտրեք էջը'),
        ),
    ]
