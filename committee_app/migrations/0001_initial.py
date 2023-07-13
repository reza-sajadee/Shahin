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
            name='Committee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(choices=[('شورا', 'شورا '), ('کمیسیون', 'کمیسیون'), ('کمیته', 'کمیته'), ('کارگروه', 'کارگروه'), ('هیأت', 'هیأت'), ('جلسه', 'جلسه'), ('سایر', 'سایر')], max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('mostanadGhanoni', models.CharField(max_length=250)),
                ('typeComittee', models.CharField(choices=[('تصمیم مدیریتی', 'تصمیم مدیریتی '), ('قانون', 'قانون'), ('دستورالعمل', 'دستورالعمل'), ('سیستم و استاندارد سازی', 'سیستم و استاندارد سازی'), ('سایر', 'سایر')], max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dabir', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dabir', to='organization_app.jobbank')),
                ('head', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='headOfCommittee', to='organization_app.jobbank')),
                ('hoze', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hozeOfCommittee', to='organization_app.hoze')),
                ('janeshinAval', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='janeshinAval', to='organization_app.jobbank')),
                ('janeshinDovom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='janeshinDovom', to='organization_app.jobbank')),
                ('members', models.ManyToManyField(related_name='members', to='organization_app.jobbank')),
            ],
            options={
                'verbose_name': 'کمیته ',
                'verbose_name_plural': 'کمیته ',
            },
        ),
    ]