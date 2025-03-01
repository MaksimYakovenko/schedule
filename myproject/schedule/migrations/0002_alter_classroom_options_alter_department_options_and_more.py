# Generated by Django 5.1.4 on 2024-12-14 18:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classroom',
            options={'ordering': ['name'], 'verbose_name': 'Аудиторія', 'verbose_name_plural': 'Аудиторії'},
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ['name'], 'verbose_name': 'Кафедра', 'verbose_name_plural': 'Кафедри'},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['weekday', 'number'], 'verbose_name': 'Заняття', 'verbose_name_plural': 'Заняття'},
        ),
        migrations.AlterModelOptions(
            name='semester',
            options={'ordering': ['-year', 'number'], 'verbose_name': 'Семестр', 'verbose_name_plural': 'Семестри'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ['full_name'], 'verbose_name': 'Викладач', 'verbose_name_plural': 'Викладачі'},
        ),
        migrations.AlterUniqueTogether(
            name='lesson',
            unique_together={('classroom', 'weekday', 'number')},
        ),
        migrations.AlterField(
            model_name='classroom',
            name='capacity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='department',
            name='faculty',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='group',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='number',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='schedule.semester'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='subject',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='weekday',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='semester',
            name='number',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='degree',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='full_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='position',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterModelTable(
            name='classroom',
            table='classroom',
        ),
        migrations.AlterModelTable(
            name='department',
            table='department',
        ),
        migrations.AlterModelTable(
            name='lesson',
            table='lesson',
        ),
        migrations.AlterModelTable(
            name='semester',
            table='semester',
        ),
        migrations.AlterModelTable(
            name='teacher',
            table='teacher',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='week_type',
        ),
    ]
