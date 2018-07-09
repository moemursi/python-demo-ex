# Generated by Django 2.0.3 on 2018-07-03 15:23

from django.db import migrations
import phonenumbers

def set_validated_phonenumber(apps, schema_editor):
    ClientOfStylist = apps.get_model('client', 'ClientOfStylist')
    for client_of_stylist in ClientOfStylist.objects.all():
        phone_number_to_save = None
        try:
            phonenumber_object = phonenumbers.parse(client_of_stylist.phone, "US")
            if phonenumbers.is_possible_number(phonenumber_object):
                phone_number_to_save = phonenumbers.format_number(
                    phonenumber_object, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            pass
        client_of_stylist.phone = phone_number_to_save
        client_of_stylist.save(update_fields=["phone"])

class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_auto_20180623_1510'),
    ]

    operations = [
        migrations.RunPython(set_validated_phonenumber, migrations.RunPython.noop),
    ]