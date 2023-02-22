# Generated by Django 3.1 on 2022-02-21 20:38

import beercity.utils
import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20220221_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='breadcrumb_image',
            field=beercity.utils.CustomLogoField(blank=True, null=True, upload_to='', verbose_name='Breadcrumb -ի նկար'),
        ),
        migrations.AlterField(
            model_name='category',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', help_text='Այս դաշտի արդյունքը երևում է գլխավոր էջի վերևի բաժիններ ֊ի հատվածում', image_field=None, max_length=18, samples=None, verbose_name='Background -ի գույն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='show_in_header',
            field=models.BooleanField(default=False, verbose_name='Ցուցադրել header -ում'),
        ),
    ]
