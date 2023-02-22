# Generated by Django 4.0.2 on 2022-02-25 21:01

import beercity.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_product_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='BonusDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Անուն')),
                ('is_active', models.BooleanField(default=True, verbose_name='Հասանելի է')),
                ('active_from', models.DateTimeField(verbose_name='Զեղչի սկիզբ')),
                ('active_to', models.DateTimeField(verbose_name='Զեղչի ավարտ')),
                ('icon', beercity.utils.CustomLogoField(upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='bonus_day_not_working',
            field=models.BooleanField(default=False, verbose_name='Անտեսել բաժնի / բաժինների վրա տարածվող զեղչը'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(to='shop.Category', verbose_name='Ընտրել բաժինը / բաժինները'),
        ),
        migrations.CreateModel(
            name='ProductIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_ingredients', to='shop.product')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='shop.product')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryBonuses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.FloatField(default=0.0, verbose_name='Զեղչի տոկոս')),
                ('bonus', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.bonusdays', verbose_name='Բոնուսի անվանում')),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bonus_days', to='shop.category', verbose_name='Բաժնի անուն')),
            ],
        ),
    ]
