# Generated by Django 2.0.13 on 2019-04-20 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0006_message_msg_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'get_latest_by': 'datetime'},
        ),
    ]
