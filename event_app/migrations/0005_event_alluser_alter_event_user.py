# Generated by Django 4.1.7 on 2023-07-18 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile_app', '0001_initial'),
        ('event_app', '0004_alter_event_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='allUser',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='event',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profileEvent', to='profile_app.profile'),
        ),
    ]
