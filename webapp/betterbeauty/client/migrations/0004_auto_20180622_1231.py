# Generated by Django 2.0.3 on 2018-06-22 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0036_auto_20180625_0219'),
        ('appointment', '0017_auto_20180625_0219'),
        ('client', '0003_auto_20180622_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='user',
        ),
        migrations.DeleteModel(
            name='Client',
        ),
    ]