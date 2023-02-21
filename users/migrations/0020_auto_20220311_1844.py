# Generated by Django 3.1 on 2022-03-11 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20220310_2245'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Ստեղծման/Ծննդյան օր'),
        ),
        migrations.AddField(
            model_name='user',
            name='company_spher',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ընկերության ոլորտ'),
        ),
        migrations.AddField(
            model_name='user',
            name='company_website',
            field=models.URLField(blank=True, null=True, verbose_name='Ընկերության ՎԵԲ կայք'),
        ),
        migrations.AddField(
            model_name='user',
            name='fact_address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ընկերության փաստացի հացե'),
        ),
        migrations.AddField(
            model_name='user',
            name='register_address',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Ընկերության գրանցման հասցե'),
        ),
        migrations.AddField(
            model_name='user',
            name='res_position',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Պատասխանատու անձի պաշտոն'),
        ),
        migrations.AddField(
            model_name='user',
            name='resfirst_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Պատասխանատու անձի անուն'),
        ),
        migrations.AddField(
            model_name='user',
            name='reslast_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Պատասխանատու անձի ազգանուն'),
        ),
        migrations.AddField(
            model_name='user',
            name='tin',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ՀՎՀՀ'),
        ),
        migrations.AlterField(
            model_name='user',
            name='company_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ընկերության անուն'),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usercity', to='users.city'),
        ),
        migrations.AddField(
            model_name='user',
            name='fact_city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factcity', to='users.city', verbose_name='Ընկերության փաստացի հասցե(քաղաք)'),
        ),
        migrations.AddField(
            model_name='user',
            name='fact_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factstate', to='users.state', verbose_name='Ընկերության փաստացի հասցե(մարզ)'),
        ),
        migrations.AddField(
            model_name='user',
            name='register_city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='regcity', to='users.city', verbose_name='Ընկերության գրանցման հասցե(քաղաք)'),
        ),
        migrations.AddField(
            model_name='user',
            name='register_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='regstate', to='users.state', verbose_name='Ընկերության գրանցման հասցե(մարզ)'),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userstate', to='users.state'),
        ),
    ]
