# Generated by Django 2.0.13 on 2019-04-20 05:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_auto_20190414_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='classroom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.Classroom'),
        ),
    ]
