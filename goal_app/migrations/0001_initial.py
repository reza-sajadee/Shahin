# Generated by Django 4.1.7 on 2023-06-13 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('principle', models.CharField(blank=True, max_length=250, null=True, verbose_name='اصل')),
                ('presppective', models.CharField(blank=True, max_length=250, null=True, verbose_name='منظر')),
                ('goal', models.CharField(blank=True, max_length=250, null=True, verbose_name='هدف کلان')),
                ('title', models.CharField(blank=True, max_length=250, null=True, verbose_name='عنوان')),
                ('index', models.CharField(blank=True, max_length=250, null=True, verbose_name='شاخص')),
                ('trendIndex', models.CharField(blank=True, choices=[('upTrend', 'روند افزایشی'), ('downTrend', 'روند کاهشی'), ('side', 'روند ثابت')], max_length=250, null=True, verbose_name='روند شاخص')),
                ('target', models.CharField(blank=True, max_length=250, null=True, verbose_name='معیار')),
                ('currentSituation', models.CharField(blank=True, max_length=250, null=True, verbose_name='وضعیت موجود')),
                ('startLine', models.DateTimeField(blank=True, null=True)),
                ('deadLine', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nextObjective', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='NeObjective', to='goal_app.objective')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ownerObjective', to='organization_app.jobbank')),
                ('previousObjective', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PrObjective', to='goal_app.objective')),
            ],
            options={
                'verbose_name': ' هدف خرد ',
                'verbose_name_plural': 'هدف خرد ',
            },
        ),
    ]