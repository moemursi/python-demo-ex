# Generated by Django 2.0.3 on 2018-04-16 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0003_auto_20180413_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salon',
            name='city',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='salon',
            name='state',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='salon',
            name='zip_code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]