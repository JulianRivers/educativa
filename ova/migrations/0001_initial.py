# Generated by Django 4.1.2 on 2024-06-23 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, verbose_name='Titulo')),
                ('is_sumativo', models.BooleanField(default=False, verbose_name='sumativa')),
            ],
            options={
                'db_table': 'actividades',
            },
        ),
        migrations.CreateModel(
            name='Lecciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, verbose_name='Titulo')),
                ('link', models.CharField(max_length=100, verbose_name='Link')),
                ('template', models.CharField(max_length=255, verbose_name='Template')),
            ],
            options={
                'db_table': 'lecciones',
            },
        ),
        migrations.CreateModel(
            name='Unidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, verbose_name='Titulo')),
                ('ariaLabel', models.CharField(blank=True, max_length=100, null=True, verbose_name='Aria Label')),
            ],
            options={
                'db_table': 'unidades',
            },
        ),
        migrations.CreateModel(
            name='ProgresoLeccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progreso', models.IntegerField(default=0)),
                ('completado', models.BooleanField(default=False)),
                ('unidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ova.lecciones')),
            ],
            options={
                'db_table': 'progreso_lecciones',
            },
        ),
    ]
