# Generated by Django 2.0.3 on 2018-06-17 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0012_appointmentservice_applied_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentservice',
            name='discount_percentage',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
