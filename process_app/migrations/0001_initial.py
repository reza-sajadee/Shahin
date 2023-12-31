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
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('groupCode', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Nahiye',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('nahiyeCode', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('processCode', models.CharField(max_length=15)),
                ('impactFactor', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groupCode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group', to='process_app.group')),
                ('ownerVahed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='OwnerVahed', to='organization_app.vahed')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goalProcess', models.TextField(blank=True, null=True)),
                ('driverProcess', models.TextField(blank=True, null=True)),
                ('scopeProcess', models.CharField(blank=True, max_length=250, null=True)),
                ('guidelinesProcess', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('process', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='process', to='process_app.process')),
            ],
            options={
                'verbose_name': ' شناسنامه فرآیند',
                'verbose_name_plural': ' شناسنامه فرآیند',
            },
        ),
        migrations.CreateModel(
            name='ProcessTo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outputProcess', models.TextField(blank=True, null=True)),
                ('toBeneficiary', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ProcessDocumentRealated', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProcessDocumentRealatedTo', to='process_app.processdocument')),
                ('toProcessRelated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='toProcessRelated', to='process_app.process')),
            ],
            options={
                'verbose_name': ' به فرآیند',
                'verbose_name_plural': ' به فرآیند',
            },
        ),
        migrations.CreateModel(
            name='ProcessFrom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inputProcess', models.TextField(blank=True, null=True)),
                ('fromBeneficiary', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ProcessDocumentRealated', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProcessDocumentRealatedFrom', to='process_app.processdocument')),
                ('fromProcessRelated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fromProcessRelated', to='process_app.process')),
            ],
            options={
                'verbose_name': ' از فرآیند',
                'verbose_name_plural': ' از فرآیند',
            },
        ),
        migrations.CreateModel(
            name='ProcessDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activityDescription', models.TextField(blank=True, null=True)),
                ('ownerActivity', models.CharField(blank=True, max_length=250, null=True)),
                ('activityDocumentation', models.CharField(blank=True, max_length=250, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('activityCondition', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ProcessDocumentRelated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ProcessDocument', to='process_app.processdocument')),
            ],
            options={
                'verbose_name': ' شرح فرآیند',
                'verbose_name_plural': ' شرح فرآیند',
            },
        ),
        migrations.CreateModel(
            name='Hoze',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('hozeCode', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nahiyeCode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nahiye', to='process_app.nahiye')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='hozeCode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hoze', to='process_app.hoze'),
        ),
    ]
