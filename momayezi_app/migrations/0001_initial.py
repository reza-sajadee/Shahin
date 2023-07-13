# Generated by Django 4.1.7 on 2023-06-13 17:27

from django.db import migrations, models
import django.db.models.deletion
import momayezi_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('standardTable_app', '0001_initial'),
        ('profile_app', '0001_initial'),
        ('organization_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalenderMomayezi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateMomayezi', models.DateTimeField(blank=True, null=True)),
                ('timeStart', models.TimeField(blank=True, null=True)),
                ('timeDuration', models.TimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bandMomayezi', models.ManyToManyField(related_name='bandMomayeziCalender', to='standardTable_app.requirementstandards')),
                ('systemMomayezi', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='systemMomayezi', to='standardTable_app.standard')),
            ],
            options={
                'verbose_name': 'زمانبندی ممیزی',
                'verbose_name_plural': 'زمانبندی ممیزی',
            },
        ),
        migrations.CreateModel(
            name='MomayeziActivityManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('done', 'انجام شده'), ('doing', 'درحال انجام'), ('doNot', 'انجام نشد')], default='doing', max_length=75)),
                ('activity', models.CharField(choices=[('team', 'تعریف تیم'), ('calender', 'برنامه زمانی'), ('cheakListQuestion', 'چک لیست سوال'), ('cheakList', 'چک لیست'), ('report', 'گزارش'), ('finish', 'پایان')], max_length=75)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('calender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='calenderMomayeziActivity', to='momayezi_app.calendermomayezi')),
                ('nextActivity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='NeActivityMomayezi', to='momayezi_app.momayeziactivitymanager')),
                ('previousActivity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PrActivityMomayezi', to='momayezi_app.momayeziactivitymanager')),
                ('reciver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ReciverProfileMomayezi', to='profile_app.profile')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='SenderProfileMomayezi', to='profile_app.profile')),
            ],
            options={
                'verbose_name': 'مدیریت فعالیت های ممیزی   ',
                'verbose_name_plural': 'مدیریت فعالیت های ممیزی   ',
            },
        ),
        migrations.CreateModel(
            name='MomayeziTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('memberMomayezi', models.ManyToManyField(related_name='memberMomayeziTeam', to='profile_app.profile')),
                ('sarMomayez', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sarMomayez', to='profile_app.profile')),
                ('standardRelated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='standardRelated', to='standardTable_app.standard')),
            ],
            options={
                'verbose_name': 'تیم ممیزی',
                'verbose_name_plural': 'تیم ممیزی',
            },
        ),
        migrations.CreateModel(
            name='RoleMomayezi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'نقش های ممیزی',
                'verbose_name_plural': 'نقش های ممیزی',
            },
        ),
        migrations.CreateModel(
            name='TypeMomayezi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('typeMomayeziCode', models.CharField(max_length=100)),
                ('step', models.CharField(choices=[('1', 'تعریف تیم'), ('2', 'برنامه زمانی'), ('3', 'چک لیست سوال'), ('4', 'چک لیست'), ('5', 'گزارش'), ('6', 'پایان')], default='1', max_length=75)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('modir', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modirMomayezi', to='profile_app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='ReportMomayezi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.CharField(max_length=100)),
                ('result', models.CharField(choices=[('ghovat', 'نقطه قوت'), ('behbod', 'فرصت بهبود'), ('adam', 'عدم انطباق')], default='ghovat', max_length=75)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('activityRelated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activityRelatedReport', to='momayezi_app.momayeziactivitymanager')),
                ('typeMomayeziRelated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='typeMomayeziRelatedReport', to='momayezi_app.typemomayezi')),
                ('vahedRelated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vahedRelatedReport', to='organization_app.vahed')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionMomayeziList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('requirementStandardQuestion', models.ManyToManyField(related_name='requirementStandardQuestion', to='standardTable_app.requirementstandards')),
                ('standardQuestion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='standardQuestion', to='standardTable_app.standard')),
                ('vahedQuestion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vahedQuestion', to='organization_app.vahed')),
            ],
            options={
                'verbose_name': 'سوالات ممیزی  ',
                'verbose_name_plural': 'سوالات ممیزی  ',
            },
        ),
        migrations.CreateModel(
            name='NoghatGhovat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('calenderGhovat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='calenderGhovat', to='momayezi_app.calendermomayezi')),
                ('systemGhovat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='systemGhovat', to='standardTable_app.standard')),
                ('teamGhovat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teamGhovat', to='momayezi_app.momayeziteam')),
                ('typeMomayeziRelated', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='typeMomayeziRelatedGovat', to='momayezi_app.typemomayezi')),
                ('vahedGhovat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vahedGhovat', to='organization_app.vahed')),
            ],
        ),
        migrations.CreateModel(
            name='MomayeziTeamRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sabegheYear', models.IntegerField(blank=True, null=True)),
                ('document', models.FileField(blank=True, null=True, upload_to=momayezi_app.models.user_directory_path)),
                ('status', models.CharField(choices=[('accept', 'accept'), ('reject', 'reject'), ('not', 'not')], default='not', max_length=75)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('memberMomayezi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='memberMomayeziRequest', to='profile_app.profile')),
            ],
            options={
                'verbose_name': 'درخواست عضویت در تیم ممیزی',
                'verbose_name_plural': 'درخواست عضویت در تیم ممیزی',
            },
        ),
        migrations.AddField(
            model_name='momayeziteam',
            name='typeMomayeziRelated',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='typeMomayeziTeam', to='momayezi_app.typemomayezi'),
        ),
        migrations.AddField(
            model_name='momayeziteam',
            name='vahedMomayezi',
            field=models.ManyToManyField(related_name='vahedMomayeziTeam', to='organization_app.vahed'),
        ),
        migrations.AddField(
            model_name='momayeziactivitymanager',
            name='typeMomayeziRelated',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='typeMomeyeziRelatedActivity', to='momayezi_app.typemomayezi'),
        ),
        migrations.CreateModel(
            name='ForsatBehbod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('calenderBehbod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='calenderBehbod', to='momayezi_app.calendermomayezi')),
                ('systemBehbod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='systemBehbod', to='standardTable_app.standard')),
                ('teamBehbod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teamBehbod', to='momayezi_app.momayeziteam')),
                ('typeMomayeziRelated', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='typeMomayeziRelatedBehbod', to='momayezi_app.typemomayezi')),
                ('vahedBehbod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vahedBehbod', to='organization_app.vahed')),
            ],
        ),
        migrations.CreateModel(
            name='CheckListMomayezi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('observed', models.TextField(blank=True, null=True)),
                ('result', models.CharField(blank=True, choices=[('ok', 'ok'), ('Obs', 'Obs'), ('min', 'min'), ('maj', 'maj')], max_length=75, null=True)),
                ('document', models.FileField(blank=True, null=True, upload_to=momayezi_app.models.user_directory_path_checklist)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activityCheckListMomayezi', to='momayezi_app.momayeziactivitymanager')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questionCheckListMomayezi', to='momayezi_app.questionmomayezilist')),
                ('typeMomayeziRelated', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='typeMomayeziRelatedCheckList', to='momayezi_app.typemomayezi')),
            ],
            options={
                'verbose_name': 'چک لیست ممیزی',
                'verbose_name_plural': 'چک لیست ممیزی',
            },
        ),
        migrations.AddField(
            model_name='calendermomayezi',
            name='teamMomayezi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MomayeziTeam', to='momayezi_app.momayeziteam'),
        ),
        migrations.AddField(
            model_name='calendermomayezi',
            name='vahedMomayezi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vahedMomayezi', to='organization_app.vahed'),
        ),
        migrations.CreateModel(
            name='AdamEntebagh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bandMomayeziAdamEntebagh', models.ManyToManyField(related_name='bandMomayeziAdamEntebagh', to='standardTable_app.requirementstandards')),
                ('calenderAdamEntebagh', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='calenderAdamEntebagh', to='momayezi_app.calendermomayezi')),
                ('systemAdamEntebagh', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='systemAdamEntebagh', to='standardTable_app.standard')),
                ('teamAdamEntebagh', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teamAdamEntebagh', to='momayezi_app.momayeziteam')),
                ('typeMomayeziRelated', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='typeMomayeziRelatedAdam', to='momayezi_app.typemomayezi')),
                ('vahedAdamEntebagh', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vahedAdamEntebagh', to='organization_app.vahed')),
            ],
        ),
    ]