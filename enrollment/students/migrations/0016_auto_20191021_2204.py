# Generated by Django 2.0.13 on 2019-10-22 05:04

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0015_auto_20191021_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='student',
            name='classrooms',
            field=models.ManyToManyField(to='students.Classroom'),
        ),
    ]
