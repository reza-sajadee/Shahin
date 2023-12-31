# Generated by Django 4.1.7 on 2023-07-16 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0002_alter_event_display_alter_event_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='color',
            field=models.CharField(blank=True, choices=[('#F44335 ', 'قرمز'), ('#4CAF50', 'سبز'), ('#fb8c00', 'نارنجی')], default='سبز', max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
