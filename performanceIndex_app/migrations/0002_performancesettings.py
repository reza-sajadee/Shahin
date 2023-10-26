# Generated by Django 4.1.7 on 2023-07-29 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performanceIndex_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerformanceSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startPeriod', models.IntegerField()),
                ('endPeriod', models.IntegerField()),
            ],
            options={
                'verbose_name': 'نمظیمات شاخص',
                'verbose_name_plural': 'نمظیمات شاخص',
            },
        ),
    ]
