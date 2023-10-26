# Generated by Django 4.1.7 on 2023-08-06 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='source',
            field=models.CharField(choices=[('personal', 'شخصی'), ('meeting', 'جلسه'), ('corrective', 'اقدام اصلاحی'), ('mostanadat', 'مستندات')], default='personal', max_length=75),
        ),
    ]
