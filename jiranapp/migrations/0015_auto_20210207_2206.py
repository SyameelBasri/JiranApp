# Generated by Django 2.2.5 on 2021-02-07 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jiranapp', '0014_auto_20190930_2019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facilitybooking',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='facilitybooking',
            name='start_time',
        ),
        migrations.AlterField(
            model_name='facilitybooking',
            name='date',
            field=models.DateTimeField(verbose_name='Booking date'),
        ),
    ]
