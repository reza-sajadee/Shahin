# Generated by Django 4.1.7 on 2023-07-18 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('momayezi_app', '0002_remove_typemomayezi_typemomayezicode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportmomayezi',
            name='report',
            field=models.CharField(max_length=250),
        ),
    ]
