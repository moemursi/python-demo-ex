# Generated by Django 2.0.3 on 2018-07-26 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0045_auto_20180724_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='stylist',
            name='instagram_url',
            field=models.CharField(blank=True, max_length=2084, null=True),
        ),
        migrations.AddField(
            model_name='stylist',
            name='website_url',
            field=models.CharField(blank=True, max_length=2084, null=True),
        ),
    ]
