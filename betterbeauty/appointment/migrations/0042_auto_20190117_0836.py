# Generated by Django 2.1 on 2019-01-17 13:36
from decimal import Decimal

from django.db import migrations, transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce


@transaction.atomic
def fix_discount_amount_on_appointments(apps, schema_editor):
    Appointment = apps.get_model('appointment', 'Appointment')
    appointments_to_populate = Appointment.objects.filter(
        service__isnull=False,
        total_discount_percentage__gt=0,
        total_discount_amount=0
    )
    for appointment in appointments_to_populate.iterator():
        services_costs = appointment.services.aggregate(
            total_before_tax=Coalesce(Sum('client_price'), Decimal(0)),
            total_regular=Coalesce(Sum('regular_price'), Decimal(0))
        )
        total_discount_amount = max(
            services_costs['total_regular'] - services_costs['total_before_tax'],
            Decimal(0)
        )
        appointment.total_discount_amount = total_discount_amount
        appointment.save(update_fields=['total_discount_amount', ])


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0041_auto_20190116_0936'),
    ]

    operations = [
        migrations.RunPython(fix_discount_amount_on_appointments, migrations.RunPython.noop)
    ]
