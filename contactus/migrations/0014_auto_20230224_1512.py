# Generated by Django 3.1 on 2023-02-24 11:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contactus', '0013_auto_20230110_1647'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ստեղծման օր')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ձևափոխման օր')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('message', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Հետադարձ կապ',
                'verbose_name_plural': 'Հետադարձ կապ',
            },
        ),
        migrations.RemoveField(
            model_name='bookings',
            name='time_of_pick',
        ),
        migrations.DeleteModel(
            name='ContactUsRequest',
        ),
        migrations.RemoveField(
            model_name='contactusjoinusdata',
            name='created',
        ),
        migrations.RemoveField(
            model_name='contactusjoinusdata',
            name='text_en',
        ),
        migrations.RemoveField(
            model_name='contactusjoinusdata',
            name='text_hy',
        ),
        migrations.RemoveField(
            model_name='contactusjoinusdata',
            name='text_ru',
        ),
        migrations.RemoveField(
            model_name='contactusjoinusdata',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='contactuspage',
            name='created',
        ),
        migrations.RemoveField(
            model_name='contactuspage',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='followuscontactus',
            name='created',
        ),
        migrations.RemoveField(
            model_name='followuscontactus',
            name='updated',
        ),
        migrations.AddField(
            model_name='contactusjoinusdata',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Ստեղծման օր'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactusjoinusdata',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Ձևափոխման օր'),
        ),
        migrations.AlterField(
            model_name='contactusjoinusdata',
            name='contact_us',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_icons', to='contactus.contactuspage'),
        ),
        migrations.AlterField(
            model_name='contactusjoinusdata',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='contactuspage',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='followuscontactus',
            name='contact_us',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_buttons', to='contactus.contactuspage'),
        ),
        migrations.AlterField(
            model_name='followuscontactus',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.DeleteModel(
            name='Bookings',
        ),
        migrations.DeleteModel(
            name='WorkingHours',
        ),
    ]
