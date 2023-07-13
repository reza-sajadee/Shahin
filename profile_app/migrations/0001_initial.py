# Generated by Django 4.1.7 on 2023-06-13 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employeeNumber', models.IntegerField(default=0)),
                ('firstName', models.CharField(max_length=250)),
                ('lastName', models.CharField(max_length=250)),
                ('idNumber', models.IntegerField(blank=True, null=True)),
                ('birthDate', models.DateField(blank=True, null=True)),
                ('bakhshShoghliCode', models.CharField(blank=True, max_length=250, null=True)),
                ('rotbeFardi', models.CharField(blank=True, max_length=250, null=True)),
                ('is_Married', models.CharField(choices=[('مجرد', 'مجرد'), ('متاهل', 'متاهل')], default='مجرد', max_length=50)),
                ('estekhdamStatus', models.CharField(choices=[('دایم', 'دایم'), ('مدت معین', 'مدت معین'), ('خدماتی حجمی', 'خدماتی حجمی'), ('خدماتی تامین نیرو', 'خدماتی تامین نیرو'), ('سایر', 'سایر')], default='سایر', max_length=75)),
                ('postSazmaniCodeManual', models.CharField(blank=True, max_length=250, null=True)),
                ('sabegheKharejSanaat', models.CharField(blank=True, max_length=250, null=True)),
                ('tahsilatType', models.CharField(choices=[('دیپلم', 'دیپلم'), ('فوق دیپلم', 'فوق دیپلم'), ('لیسانس', 'لیسانس'), ('فوق لیسانس', 'فوق لیسانس'), ('دکتری', 'دکتری'), ('سایر', 'سایر')], default='سایر', max_length=100)),
                ('vaziyat', models.CharField(choices=[('شاغل', 'شاغل')], default='شاغل', max_length=100)),
                ('genderType', models.CharField(choices=[('مرد', 'مرد'), ('زن', 'زن')], default='مرد', max_length=100)),
                ('IsargarType', models.CharField(choices=[('ایثارگر', 'ایثارگر'), ('غیر ایثارگر', 'غیر ایثارگر')], default='غیر ایثارگر', max_length=100)),
                ('reshte', models.CharField(blank=True, max_length=250, null=True)),
                ('sandoghBazneshastegi', models.CharField(blank=True, max_length=250, null=True)),
                ('sherkat', models.CharField(default='شركت آب و فاضلاب منطقه يك شهر تهران', max_length=250)),
                ('sathePost', models.CharField(blank=True, max_length=250, null=True)),
                ('takalof', models.IntegerField(default=0)),
                ('etmameKhedmat', models.CharField(blank=True, max_length=250, null=True)),
                ('nameSherkathayeOstan', models.CharField(default='4', max_length=250)),
                ('tarikhShoroKhedmat', models.DateField(blank=True, null=True)),
                ('sherkatCode', models.IntegerField(blank=True, default=4, null=True)),
                ('city', models.CharField(blank=True, max_length=250, null=True)),
                ('sherkateMabda', models.CharField(blank=True, max_length=250, null=True)),
                ('sabegheDakhelSanaat', models.CharField(blank=True, max_length=250, null=True)),
                ('tarigheJazb', models.CharField(blank=True, max_length=250, null=True)),
                ('estekhdamType', models.CharField(default='کارگری', max_length=250)),
                ('din', models.CharField(default='مسلمان', max_length=250)),
                ('dateChanged', models.CharField(blank=True, max_length=250, null=True)),
                ('sherkateMaghsad', models.CharField(blank=True, max_length=250, null=True)),
                ('mazhab', models.CharField(default='شیعه', max_length=250)),
                ('reshteShoghl', models.CharField(blank=True, max_length=250, null=True)),
                ('lastMadrakDate', models.DateField(blank=True, null=True)),
                ('vaziyatPostSazmani', models.CharField(blank=True, default='مصوب', max_length=100, null=True)),
                ('radifPostSazmani', models.CharField(blank=True, max_length=100, null=True)),
                ('daneshgahType', models.CharField(blank=True, max_length=100, null=True)),
                ('familyNumbers', models.IntegerField(default=0)),
                ('halateIsargari', models.CharField(blank=True, max_length=100, null=True)),
                ('majmoeHoghogh', models.IntegerField(blank=True, null=True)),
                ('ozviyatModire', models.CharField(default='عدم عضو', max_length=100)),
                ('fatherName', models.CharField(blank=True, max_length=100, null=True)),
                ('shenasnameCode', models.IntegerField(blank=True, null=True)),
                ('phoneNumber', models.IntegerField(blank=True, null=True)),
                ('tellNumber', models.IntegerField(blank=True, null=True)),
                ('bloodType', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('نامشخص', 'نامشخص')], default='O+', max_length=100)),
                ('sherkatPeymankar', models.CharField(blank=True, default='نامشخص', max_length=100, null=True)),
                ('startPardakht', models.DateField(blank=True, null=True)),
                ('eshteghalVaziyat', models.CharField(blank=True, max_length=100, null=True)),
                ('cityBorn', models.CharField(blank=True, max_length=100, null=True)),
                ('citySodor', models.CharField(blank=True, max_length=100, null=True)),
                ('titleShoghlMoredTasadi', models.CharField(blank=True, max_length=100, null=True)),
                ('vorodBeSherkathayeOstaneDate', models.DateField(blank=True, null=True)),
                ('taminEjtemaiSabeghe', models.IntegerField(blank=True, null=True)),
                ('nezameEstekhdami', models.IntegerField(blank=True, null=True)),
                ('sabegheBeTarikhTaminEjtemai', models.CharField(blank=True, max_length=101, null=True)),
                ('sabegheBeRozVorodBeSherkat', models.IntegerField(blank=True, null=True)),
                ('janamayi', models.CharField(blank=True, max_length=100, null=True)),
                ('indexmahalekhedmat', models.CharField(blank=True, max_length=100, null=True)),
                ('postSazmaniTitleManual', models.CharField(blank=True, max_length=100, null=True)),
                ('shomarande', models.CharField(blank=True, max_length=100, null=True)),
                ('shoghlSazmaniCode', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
