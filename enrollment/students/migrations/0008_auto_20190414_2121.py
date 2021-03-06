# Generated by Django 2.0.13 on 2019-04-15 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_auto_20190414_1813'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classroom',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='site',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='classroom',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.Site'),
        ),
        migrations.AlterField(
            model_name='student',
            name='classroom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.Classroom'),
        ),
    ]
