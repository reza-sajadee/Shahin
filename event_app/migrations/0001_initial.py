# Generated by Django 4.1.7 on 2023-06-13 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profile_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField()),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('color', models.CharField(blank=True, choices=[('#F44335 ', 'قرمز'), ('#4CAF50', 'سبز'), ('#fb8c00', 'نارنجی')], max_length=8, null=True)),
                ('display', models.CharField(blank=True, choices=[('auto', 'خودکار'), ('list-item', 'نقطه')], default='auto', max_length=20, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profileEvent', to='profile_app.profile')),
            ],
            options={
                'verbose_name': ' رویداد',
                'verbose_name_plural': ' رویداد',
            },
        ),
    ]
