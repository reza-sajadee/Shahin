# Generated by Django 4.1.7 on 2023-10-03 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0005_action_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='status',
            field=models.CharField(blank=True, choices=[('complate', 'اتمام شده'), ('doing', 'در حال انجام'), ('done', 'انجام شد')], default='doing', max_length=250, null=True, verbose_name='وضعیت'),
        ),
    ]
