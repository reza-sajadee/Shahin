# Generated by Django 4.1.7 on 2023-08-22 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performanceIndex_app', '0005_alter_performanceindexactivitymanager_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='performanceformula',
            name='acceptableCriteriaSecond',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
