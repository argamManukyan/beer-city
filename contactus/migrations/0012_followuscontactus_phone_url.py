# Generated by Django 3.2.7 on 2023-01-10 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactus', '0011_contactuspage_contact_bg_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='followuscontactus',
            name='phone_url',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Mobile -ի Հղում'),
        ),
    ]
