# Generated by Django 2.1 on 2018-10-10 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0019_client_location_from_zipcode'),
        ('salon', '0053_auto_20180906_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='created_real_client',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='client.Client'),
        ),
    ]
