# Generated by Django 2.0.13 on 2019-10-22 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0016_auto_20191021_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='classrooms',
            field=models.ManyToManyField(to='students.Classroom'),
        ),
    ]
