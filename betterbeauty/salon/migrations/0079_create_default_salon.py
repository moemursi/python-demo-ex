# Generated by Django 2.1 on 2018-12-14 06:34
from django.contrib.gis.db.backends.postgis.schema import PostGISSchemaEditor
from django.db import migrations
from django.db.migrations.state import StateApps


def create_default_salon(apps: StateApps, schema_editor: PostGISSchemaEditor):
    Stylist = apps.get_model('salon', 'Stylist')
    Salon = apps.get_model('salon', 'Salon')
    stylists = Stylist.objects.filter(salon=None)
    for stylist in stylists:
        stylist.salon = Salon.objects.create()
        stylist.save()


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0078_servicecategory_weight'),
    ]

    operations = [
        migrations.RunPython(
            create_default_salon, migrations.RunPython.noop
        )
    ]
