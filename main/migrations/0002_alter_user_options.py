# Generated by Django 5.1.1 on 2024-09-23 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('can_modify_processes', 'Can modify processes'), ('can_view_process_logs', 'Can view process logs')]},
        ),
    ]
