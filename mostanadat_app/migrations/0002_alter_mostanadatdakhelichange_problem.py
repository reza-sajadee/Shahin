# Generated by Django 4.1.7 on 2023-07-29 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mostanadat_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mostanadatdakhelichange',
            name='problem',
            field=models.CharField(blank=True, choices=[('create', 'تدوین سند'), ('edit', 'اصلاح سند'), ('delete', 'حذف سند')], max_length=75, null=True),
        ),
    ]
