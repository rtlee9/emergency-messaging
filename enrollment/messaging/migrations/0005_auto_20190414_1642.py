# Generated by Django 2.0.13 on 2019-04-14 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0004_message_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messagestatus',
            options={'get_latest_by': 'datetime'},
        ),
    ]
