# Generated by Django 4.1.7 on 2023-10-01 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0003_action_starttime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='action',
            old_name='startTime',
            new_name='startTiem',
        ),
    ]
