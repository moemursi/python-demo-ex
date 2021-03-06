# Generated by Django 2.0.3 on 2018-07-30 12:49

from django.db import migrations, models
import salon.types


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0046_auto_20180726_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='status',
            field=models.CharField(choices=[('invited', 'Invited'), ('accepted', 'Accepted')], default=salon.types.InvitationStatus('invited'), max_length=15),
        ),
    ]
