# Generated by Django 2.2.5 on 2021-02-07 14:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jiranapp', '0015_auto_20210207_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilitybooking',
            name='end_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
