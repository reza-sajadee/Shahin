# Generated by Django 4.1.7 on 2023-10-01 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performanceIndex_app', '0006_performanceformula_acceptablecriteriasecond'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performanceformula',
            name='acceptableCondition',
            field=models.CharField(blank=True, choices=[('smaller', 'کوچکتر'), ('bigger', 'بزرگتر'), ('equal', 'برابر'), ('beetween', 'بین')], max_length=75, null=True),
        ),
    ]
