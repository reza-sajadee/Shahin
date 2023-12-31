# Generated by Django 4.1.7 on 2023-07-16 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='display',
            field=models.CharField(blank=True, choices=[('auto', 'خودکار'), ('list-item', 'نقطه')], default='list-item', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateField(blank=True, null=True),
        ),
    ]
