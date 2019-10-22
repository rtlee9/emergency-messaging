# Generated by Django 2.0.13 on 2019-10-22 05:02

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0014_auto_20191021_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='classrooms',
            field=models.ManyToManyField(to='students.Classroom'),
        ),
    ]
