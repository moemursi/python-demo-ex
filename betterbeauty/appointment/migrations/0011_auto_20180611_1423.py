# Generated by Django 2.0.3 on 2018-06-11 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0010_auto_20180604_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='grand_total',
            field=models.DecimalField(decimal_places=0, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='has_card_fee_included',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='appointment',
            name='has_tax_included',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='appointment',
            name='total_card_fee',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='total_client_price_before_tax',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='total_tax',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
    ]