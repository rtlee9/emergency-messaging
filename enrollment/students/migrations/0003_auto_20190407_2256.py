# Generated by Django 2.0.13 on 2019-04-08 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20190407_2253'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ['address_1']},
        ),
    ]
