# Generated by Django 2.0.3 on 2018-06-12 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0030_auto_20180607_0656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stylistservice',
            name='service_uuid',
        ),
    ]