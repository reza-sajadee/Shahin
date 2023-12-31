# Generated by Django 4.1.7 on 2023-08-01 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting_app', '0002_alter_meetinginvitation_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='memberType',
            field=models.CharField(choices=[('pr', 'اعضای اصلی'), ('sc', 'اعضای فرعی'), ('other', 'سایر')], default='pr', max_length=100),
        ),
        migrations.AddField(
            model_name='member',
            name='otherPerson',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
