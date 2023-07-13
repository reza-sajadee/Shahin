# Generated by Django 4.1.7 on 2023-06-13 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('standardTable_app', '0001_initial'),
        ('profile_app', '0001_initial'),
        ('process_app', '0001_initial'),
        ('organization_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoolDataBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('boolean', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'دیتابیس  bool',
                'verbose_name_plural': 'دیتابیس  bool',
            },
        ),
        migrations.CreateModel(
            name='SubjectPerformanceIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'سرفصل عملکردی',
                'verbose_name_plural': 'سرفصل عملکردی',
            },
        ),
        migrations.CreateModel(
            name='TextDataBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'دیتابیس متن ها',
                'verbose_name_plural': 'دیتابیس متن ها',
            },
        ),
        migrations.CreateModel(
            name='VariableDataBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('code', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responsibleProfileVariablePerformanceFormula', to='organization_app.jobbank', verbose_name='مسئول وارد کردن ')),
            ],
            options={
                'verbose_name': 'متغیر',
                'verbose_name_plural': 'متغیر',
            },
        ),
        migrations.CreateModel(
            name='TopicPerformanceIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('subjectRelated', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topicSubjectRelated', to='performanceIndex_app.subjectperformanceindex')),
            ],
            options={
                'verbose_name': 'محور عملکردی',
                'verbose_name_plural': 'محور عملکردی',
            },
        ),
        migrations.CreateModel(
            name='PerformanceIndexActivityManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('done', 'done'), ('doing', 'doing'), ('completed', 'completed')], default='doing', max_length=75)),
                ('activity', models.CharField(choices=[], max_length=75)),
                ('startTime', models.DateField(blank=True, null=True)),
                ('deadLine', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bools', models.ManyToManyField(related_name='BoolDataPerformanceIndex', to='performanceIndex_app.booldatabase')),
                ('nextActivity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='NeActivityPerformanceIndex', to='performanceIndex_app.performanceindexactivitymanager')),
                ('previousActivity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PrActivityPerformanceIndex', to='performanceIndex_app.performanceindexactivitymanager')),
                ('reciver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ReciverProfilePErformanceIndex', to='profile_app.profile')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='SenderProfilePErformanceIndex', to='profile_app.profile')),
                ('texts', models.ManyToManyField(related_name='textDataPerformanceIndex', to='performanceIndex_app.textdatabase')),
            ],
            options={
                'verbose_name': 'مدیریت فعالیت های شاخص عملکردی    ',
                'verbose_name_plural': 'مدیریت فعالیت های شاخص عملکردی    ',
            },
        ),
        migrations.CreateModel(
            name='PerformanceIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('codePerformanceIndex', models.CharField(max_length=100)),
                ('indexType', models.CharField(choices=[('Effectiveness', 'اثربخشی'), ('Performance', 'کارایی')], max_length=100)),
                ('reference', models.CharField(max_length=100)),
                ('stackHolder', models.CharField(max_length=100)),
                ('document', models.FileField(blank=True, null=True, upload_to='performance_index_document/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('processRelated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ProcessRelatedPerformanceIndex', to='process_app.process')),
                ('standardRelated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='standardRelatedPerformanceIndex', to='standardTable_app.standard')),
            ],
            options={
                'verbose_name': 'معیار عملکردی',
                'verbose_name_plural': 'معیار عملکردی',
            },
        ),
        migrations.CreateModel(
            name='PerformanceFormula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acceptableCondition', models.CharField(blank=True, choices=[('smaller', 'کوچکتر'), ('bigger', 'بزرگتر'), ('equal', 'برابر')], max_length=75, null=True)),
                ('acceptableCriteria', models.FloatField(blank=True, null=True)),
                ('cycle', models.CharField(blank=True, choices=[('monthly', 'ماهانه'), ('seasonal', 'سه ماهه'), ('semiAnnualy', 'شش ماهه'), ('annualy', 'سالانه')], max_length=75, null=True)),
                ('metric', models.CharField(max_length=100)),
                ('PerformanceFormula', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('performanceIndexRelated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='performanceRelatedFormula', to='performanceIndex_app.performanceindex')),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responsibleProfilePerformanceFormula', to='organization_app.jobbank', verbose_name='مسئول پایش شاخص')),
                ('variablesRelated', models.ManyToManyField(to='performanceIndex_app.variabledatabase')),
            ],
            options={
                'verbose_name': 'فرمول شاخص عملکردی',
                'verbose_name_plural': 'فرمول شاخص عملکردی',
            },
        ),
        migrations.CreateModel(
            name='ConfirmationDataBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('confirm', models.CharField(choices=[('yes', 'بله'), ('no', 'خیر')], max_length=75)),
                ('text', models.TextField(blank=True, null=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PerformanceIndexConfirmProfile', to='profile_app.profile')),
            ],
            options={
                'verbose_name': 'دیتابیس  کانفرم شدن',
                'verbose_name_plural': 'دیتابیس  کانفرم شدن',
            },
        ),
    ]
