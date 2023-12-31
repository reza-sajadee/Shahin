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
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=250, null=True, verbose_name='کد')),
                ('title', models.CharField(blank=True, max_length=250, null=True, verbose_name='عنوان پروژه')),
                ('startTime', models.DateTimeField(blank=True, null=True)),
                ('deadLine', models.DateTimeField(blank=True, null=True)),
                ('index', models.CharField(blank=True, max_length=250, null=True, verbose_name='شاخص')),
                ('currentSituation', models.CharField(blank=True, max_length=250, null=True, verbose_name='وضعیت موجود')),
                ('target', models.CharField(blank=True, max_length=250, null=True, verbose_name='معیار')),
                ('resourceProject', models.CharField(blank=True, choices=[('Objective', 'هدف خرد')], default='Objective', max_length=250, null=True, verbose_name='منشا')),
                ('resourceId', models.IntegerField(blank=True, null=True, verbose_name='آی دی مرجع')),
                ('description', models.TextField(blank=True, null=True, verbose_name='منشا')),
                ('taskDependencies', models.CharField(blank=True, choices=[('predecessor', 'پیش نیاز '), ('successor', 'پس نیاز'), ('corequisite', 'همنیاز'), ('independ', 'بی ارتباط')], default='Objective', max_length=250, null=True, verbose_name='وابستگی تسک')),
                ('status', models.CharField(blank=True, choices=[('defination', 'تعریف'), ('executive', 'اجرا')], default='defination', max_length=250, null=True, verbose_name='وابستگی تسک')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('accountable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accountableProject', to='organization_app.jobbank')),
                ('controller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='controllerProject', to='organization_app.jobbank')),
                ('nextProject', models.ManyToManyField(blank=True, null=True, related_name='NeProject', to='project_app.project')),
                ('previousProject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PrProject', to='project_app.project')),
            ],
            options={
                'verbose_name': 'پروژه',
                'verbose_name_plural': 'پروژه',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True, verbose_name='عنوان اقدام')),
                ('startTime', models.DateTimeField(blank=True, null=True)),
                ('deadLine', models.DateTimeField(blank=True, null=True)),
                ('index', models.CharField(blank=True, max_length=250, null=True, verbose_name='شاخص')),
                ('requirementResource', models.CharField(blank=True, max_length=250, null=True, verbose_name='شاخص')),
                ('financialResource', models.CharField(blank=True, max_length=250, null=True, verbose_name='شاخص')),
                ('timeResource', models.CharField(blank=True, max_length=250, null=True, verbose_name='شاخص')),
                ('weightOfRequirement', models.FloatField(blank=True, null=True)),
                ('weightOfFinancial', models.FloatField(blank=True, null=True)),
                ('weightOfTime', models.FloatField(blank=True, null=True)),
                ('currentSituation', models.CharField(blank=True, max_length=250, null=True, verbose_name='وضعیت موجود')),
                ('target', models.CharField(blank=True, max_length=250, null=True, verbose_name='معیار')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('controller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='controllerTask', to='organization_app.jobbank')),
                ('nextProject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='NeProject', to='project_app.task')),
                ('previousProject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PrProject', to='project_app.task')),
                ('projectRelated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projectRelatedTask', to='project_app.project')),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responsibleTask', to='organization_app.jobbank')),
            ],
            options={
                'verbose_name': 'اقدام',
                'verbose_name_plural': 'اقدام',
            },
        ),
        migrations.CreateModel(
            name='ProjectProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True, verbose_name='عنوان پروژه')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('targetRequired', models.TextField(blank=True, null=True, verbose_name='هدف مورد نظر')),
                ('capitalEstimate', models.TextField(blank=True, null=True, verbose_name='بودجه مدنظر')),
                ('diurationEsimate', models.TextField(blank=True, null=True, verbose_name='زمان مورد نظر')),
                ('sourceProject', models.CharField(blank=True, choices=[('Objective', 'هدف خرد'), ('Other', 'سایر')], default='Objective', max_length=250, null=True, verbose_name='منشا')),
                ('sourceId', models.IntegerField(blank=True, null=True, verbose_name='آی دی مرجع')),
                ('status', models.CharField(blank=True, choices=[('defination', 'تعریف پروژه'), ('executive', 'اجرای پروژه')], default='defination', max_length=250, null=True, verbose_name='وضعیت')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('accountable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responsibleProjectProfile', to='organization_app.jobbank')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='profileProjectRelated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profileProjectRelatedProject', to='project_app.projectprofile'),
        ),
        migrations.AddField(
            model_name='project',
            name='responsible',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responsibleProject', to='organization_app.jobbank'),
        ),
        migrations.CreateModel(
            name='PlanProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True, verbose_name='عنوان برنامه اجرایی')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('sourcePlan', models.CharField(blank=True, choices=[('corrective', 'اقدام اصلاحی'), ('risk', 'ریسک'), ('meeting', 'مصوبات جلسه'), ('suggestion', 'نظام پیشنهادی'), ('goal', 'هدف'), ('other', 'سایر')], default='personal', max_length=250, null=True, verbose_name='منشا')),
                ('startTiem', models.DateTimeField(blank=True, null=True)),
                ('deadLine', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('complate', 'اتمام شده'), ('pending', 'در انتظار انجام'), ('doing', 'در حال انجام')], default='doing', max_length=250, null=True, verbose_name='وضعیت')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('accountable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accountablePlanProfile', to='organization_app.jobbank')),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responsiblePlanProfile', to='organization_app.jobbank')),
            ],
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True, verbose_name='عنوان برنامه اجرایی')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('deadLine', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('complate', 'اتمام شده'), ('pending', 'در انتظار انجام'), ('doing', 'در حال انجام'), ('done', 'انجام شد')], default='pending', max_length=250, null=True, verbose_name='وضعیت')),
                ('color', models.CharField(blank=True, choices=[('0', '--accent-color:#41516C'), ('1', '--accent-color:#FBCA3E'), ('2', '--accent-color:#E24A68'), ('3', '--accent-color:#1B5F8C'), ('4', '--accent-color:#4CADAD')], default='1', max_length=250, null=True, verbose_name='رنگ')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('planProfileRelated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='planProfileRelated', to='project_app.planprofile')),
            ],
        ),
    ]
