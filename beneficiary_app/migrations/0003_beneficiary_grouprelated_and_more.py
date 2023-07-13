# Generated by Django 4.1.7 on 2023-06-15 13:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary_app', '0002_beneficiary_classificationbeneficiary_currentneed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiary',
            name='groupRelated',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='groupRelatedBeneficiary', to='beneficiary_app.groupbeneficiary'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='currentneed',
            name='beneficiaryRelated',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='beneficiaryRelatedCurrent', to='beneficiary_app.beneficiary'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='futureexpectations',
            name='beneficiaryRelated',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='beneficiaryRelatedFuture', to='beneficiary_app.beneficiary'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='groupbeneficiary',
            name='classificationRelated',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='classificationRelatedGroup', to='beneficiary_app.classificationbeneficiary'),
            preserve_default=False,
        ),
    ]
