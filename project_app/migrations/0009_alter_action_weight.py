# Generated by Django 4.1.7 on 2023-10-05 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0008_alter_action_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='weight',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
