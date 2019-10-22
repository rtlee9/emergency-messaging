# Generated by Django 2.0.13 on 2019-10-22 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0011_auto_20190419_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.Address'),
        ),
        migrations.RemoveField(
            model_name='student',
            name='classroom',
        ),
        migrations.AddField(
            model_name='student',
            name='classroom',
            field=models.ManyToManyField(to='students.Classroom'),
        ),
    ]
