# Generated by Django 2.0.13 on 2019-04-15 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0005_auto_20190414_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='msg_type',
            field=models.CharField(default='NA', max_length=32),
            preserve_default=False,
        ),
    ]