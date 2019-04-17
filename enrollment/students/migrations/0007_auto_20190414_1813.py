# Generated by Django 2.0.13 on 2019-04-15 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_auto_20190411_2220'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.RemoveField(
            model_name='membership',
            name='class_room',
        ),
        migrations.RemoveField(
            model_name='membership',
            name='student',
        ),
        migrations.RemoveField(
            model_name='classroom',
            name='members',
        ),
        migrations.AddField(
            model_name='student',
            name='classroom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.ClassRoom'),
        ),
        migrations.DeleteModel(
            name='Membership',
        ),
        migrations.AddField(
            model_name='classroom',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.Site'),
        ),
    ]