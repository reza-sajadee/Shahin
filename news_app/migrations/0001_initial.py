# Generated by Django 4.1.7 on 2023-06-13 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoriy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': ' دسته بندی اخبار ',
                'verbose_name_plural': ' دسته بندی اخبار ',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True, verbose_name='عنوان خبر')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/news', verbose_name='عکس')),
                ('description', models.TextField(blank=True, null=True, verbose_name='متن خبر')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('NewsCategoriy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='NewsCategoriy', to='news_app.categoriy', verbose_name='دسته بندی خبر')),
            ],
            options={
                'verbose_name': '   اخبار ',
                'verbose_name_plural': '   اخبار ',
            },
        ),
    ]
