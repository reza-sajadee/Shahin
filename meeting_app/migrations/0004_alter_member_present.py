# Generated by Django 4.1.7 on 2023-08-01 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting_app', '0003_member_membertype_member_otherperson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='present',
            field=models.BooleanField(default=False),
        ),
    ]
