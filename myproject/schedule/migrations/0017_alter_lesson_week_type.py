# Generated by Django 4.2.8 on 2025-05-05 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0016_lesson_week_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='week_type',
            field=models.CharField(choices=[('even', 'Парний тиждень'), ('odd', 'Непарний тиждень'), ('both', 'Щотижня')], default='both', max_length=5),
        ),
    ]
