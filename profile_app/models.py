from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.fields.related import ForeignKey

from jalali_date import date2jalali
from django.utils import timezone

import math
class Profile(models.Model):
    
    MARRIED_TYPE_SELECT = (('مجرد','مجرد'),('متاهل','متاهل') )
    ESTEKHDAM_STATUS_SELECT = (('دایم','دایم'),('مدت معین','مدت معین') ,('خدماتی حجمی','خدماتی حجمی') ,('خدماتی تامین نیرو','خدماتی تامین نیرو') ,('سایر', 'سایر') )
    TAHSIL_TYPE_SELECT = (('دیپلم','دیپلم'),('فوق دیپلم','فوق دیپلم') ,('لیسانس','لیسانس') ,('فوق لیسانس','فوق لیسانس') ,('دکتری','دکتری'),('سایر','سایر'))
    VAZIYAT_TYPE_SELECT = (('شاغل' , 'شاغل') , )
    GENDER_TYPE_SELECT = (('مرد' , 'مرد') ,('زن' , 'زن')  )
    ISARGAR_TYPE_SELECT = (('ایثارگر' , 'ایثارگر') ,('غیر ایثارگر' , 'غیر ایثارگر')  )
    BLOOD_TYPE_SELECT = (('A+' , 'A+') ,('A-' , 'A-') ,('B+' , 'B+') ,('B-' , 'B-') ,('O+' , 'O+'),('O-' , 'O-'),('AB+' , 'AB+'),('AB-' , 'AB-'),('نامشخص' , 'نامشخص'))
    
    user      = models.OneToOneField(User , null=True  , on_delete=models.CASCADE)    
    employeeNumber  = models.IntegerField(default=0)
    firstName = models.CharField(max_length=250)
    lastName = models.CharField(max_length=250)
    idNumber = models.IntegerField(blank=True , null=True)
    birthDate = models.DateField(blank=True , null=True)
    bakhshShoghliCode = models.CharField(max_length=250 ,blank=True ,null=True)
    rotbeFardi =models.CharField(max_length=250, blank=True ,null=True)
    is_Married = models.CharField(max_length=50 ,choices= MARRIED_TYPE_SELECT , default='مجرد')
    estekhdamStatus = models.CharField(max_length=75, choices= ESTEKHDAM_STATUS_SELECT ,default='سایر' )
    postSazmaniCodeManual = models.CharField(max_length=250 , blank=True , null=True)
    sabegheKharejSanaat = models.CharField(max_length=250, blank=True, null=True)
    tahsilatType = models.CharField(max_length=100,choices= TAHSIL_TYPE_SELECT ,default='سایر')
    vaziyat = models.CharField(max_length=100 , choices =VAZIYAT_TYPE_SELECT , default='شاغل' )
    genderType = models.CharField(max_length=100, choices=GENDER_TYPE_SELECT ,default='مرد')
    IsargarType = models.CharField(max_length=100, choices=ISARGAR_TYPE_SELECT ,default='غیر ایثارگر')
    reshte = models.CharField(max_length=250 ,blank=True , null=True)
    sandoghBazneshastegi = models.CharField(max_length=250 , blank=True, null=True)
    sherkat = models.CharField(max_length=250 , default='شركت آب و فاضلاب منطقه يك شهر تهران')
    sathePost = models.CharField(max_length=250, blank=True , null=True)
    takalof = models.IntegerField(default=0)
    etmameKhedmat = models.CharField(max_length=250,blank=True , null=True)
    nameSherkathayeOstan = models.CharField(max_length=250 , default='4')
    tarikhShoroKhedmat = models.DateField( blank=True, null=True)
    sherkatCode = models.IntegerField(default=4 ,blank=True , null=True)
    
    city = models.CharField(max_length=250 , blank=True , null=True)
    sherkateMabda = models.CharField(max_length=250 , blank=True, null=True)
    sabegheDakhelSanaat = models.CharField(max_length=250, blank=True, null=True)
    tarigheJazb = models.CharField(max_length=250 , blank=True, null=True)
    estekhdamType = models.CharField(max_length=250 ,default='کارگری')
    din = models.CharField(max_length=250 ,default='مسلمان')
    dateChanged = models.CharField(max_length=250, blank=True , null=True)
    sherkateMaghsad = models.CharField(max_length=250, blank=True , null=True)
    mazhab = models.CharField(max_length=250,default="شیعه")
    reshteShoghl = models.CharField(max_length=250 , blank=True , null=True)
    lastMadrakDate = models.DateField(blank=True , null=True)
    vaziyatPostSazmani = models.CharField(max_length=100 , blank=True , null=True ,default='مصوب')
    radifPostSazmani = models.CharField(max_length=100 , blank=True , null=True)
    daneshgahType = models.CharField(max_length=100 , blank=True, null=True)
    familyNumbers = models.IntegerField(default=0)
    halateIsargari = models.CharField(max_length=100 , blank=True , null=True )
    majmoeHoghogh = models.IntegerField(blank=True , null=True)
    ozviyatModire = models.CharField(max_length=100,default='عدم عضو')
    fatherName = models.CharField(max_length=100, blank=True, null=True)
    shenasnameCode = models.IntegerField(blank=True , null=True)
    phoneNumber = models.IntegerField(blank=True , null=True)
    tellNumber = models.IntegerField(blank=True , null=True)
    bloodType = models.CharField(max_length=100,default='O+' , choices=BLOOD_TYPE_SELECT)
    sherkatPeymankar = models.CharField(max_length=100 , blank=True , null=True , default='نامشخص')
    startPardakht = models.DateField(blank=True, null=True)
    eshteghalVaziyat = models.CharField(max_length=100, blank=True , null=True)
    cityBorn = models.CharField(max_length=100 , blank=True, null=True)
    citySodor = models.CharField(max_length=100 , blank=True, null=True)
    titleShoghlMoredTasadi = models.CharField(max_length=100 , blank=True, null=True)
    vorodBeSherkathayeOstaneDate = models.DateField(blank=True , null=True)
    taminEjtemaiSabeghe = models.IntegerField(blank=True, null=True)
    nezameEstekhdami = models.IntegerField(blank=True, null=True)
    sabegheBeTarikhTaminEjtemai = models.CharField(max_length=101 , blank=True , null=True)
    sabegheBeRozVorodBeSherkat = models.IntegerField(blank=True , null=True)
    
    janamayi  = models.CharField(max_length=100 , blank=True, null=True)
    indexmahalekhedmat = models.CharField(max_length=100 , blank=True, null=True)
    postSazmaniTitleManual = models.CharField(max_length=100 , blank=True, null=True)
    shomarande = models.CharField(max_length=100 , blank=True, null=True)
    shoghlSazmaniCode = models.CharField(max_length=100 , blank=True, null=True)
    
    created_at           = models.DateTimeField(auto_now_add=True ,blank=True , null=True)
    updated_at           = models.DateTimeField(auto_now=True , blank= True , null=True)

    
    

    def __str__(self):
        return str(self.firstName + ' - ' + self.lastName)
        #return str(self.id)