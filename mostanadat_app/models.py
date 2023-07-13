from django.db import models
from django.db.models.fields.related import ForeignKey , ManyToManyField

from organization_app.models import Vahed
from organization_app.models import TypePostSazmani
from standardTable_app.models import Standard
from process_app.models import Process
from jalali_date import date2jalali 
from profile_app.models import Profile
import os
category_choices = (
    ("محرمانه", "محرمانه "),
    ("غیرمحرمانه", "غیرمحرمانه")
)
   
class TypeMadrak(models.Model):
    title                = models.CharField(max_length=100, blank=True , null=True)
    typeMadrakCode       = models.CharField(max_length=100, blank=True , null=True)
    ekhtesat             = models.CharField(max_length=100 , blank=True , null=True) 
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "نوع مدرک "
        verbose_name_plural = "نوع مدرک "
    
    def __str__(self):
        return self.title 



class MostanadatDakheli(models.Model):
    title = models.CharField(max_length=100)
    dakheliSanadCode = models.CharField(max_length=100)
    versionNumber = models.CharField(max_length=100)
    
    tabaghbandi = models.CharField(max_length=100, choices=category_choices)
    
    vahedMotevaliCode = models.ForeignKey(Vahed , blank=True, null=True, related_name="vahedMotevali" , on_delete = models.CASCADE )
    vahedTaeidCode = models.ForeignKey(TypePostSazmani , blank=True, null=True, related_name="postSazmaniTaeid" , on_delete = models.CASCADE )
    vahedTasvibCode = models.ForeignKey(TypePostSazmani , blank=True, null=True, related_name="postSazmaniTasvib" , on_delete = models.CASCADE )
    typeMadrakCode = models.ForeignKey(TypeMadrak , blank=True, null=True, related_name="refrerence" , on_delete = models.CASCADE )
    systemMortabetCode = models.ForeignKey(Standard , blank=True, null=True, related_name="systemCode" , on_delete = models.CASCADE )
    vahedMortabetCode = models.ManyToManyField(Vahed , related_name="vahedMortabet")
    
    molahezat = models.TextField( null=True, blank=True, max_length=500)
    outdated  = models.BooleanField(default=False)
    
    updated_at           = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        verbose_name = "مستندات درون سازمانی "
        verbose_name_plural = "مستندات درون سازمانی "
      
    def __str__(self):
        return self.title 
    
    def get_jalali_date(self):
        return date2jalali(self.updated_at)
    

class MostanadatKhareji(models.Model):
    title = models.CharField(max_length=100)
    kharejiSanadCode = models.CharField(max_length=100 ,blank=True , null=True)
    processCode = models.ForeignKey(Process , blank=True, null=True, related_name="procesCode" , on_delete = models.CASCADE )
    
    
    versionNumber = models.CharField(max_length=100 , blank=True , null=True)
    
    
    entesharDate = models.CharField(max_length=100 , blank=True , null=True)
    etebarDate = models.CharField(max_length=100 , blank=True , null=True)
    refrenceName = models.CharField(max_length=250,blank=True , null=True)
    expiredDate  = models.CharField(max_length=250,blank=True , null=True)
    postmasolUpdate = models.ForeignKey(TypePostSazmani , blank=True, null=True, related_name="postMasol" , on_delete = models.CASCADE )
    updatePeriod = models.CharField(max_length=100 , blank=True , null=True)
    tozihat = models.TextField( null=True, blank=True, max_length=500)
    govermentUpdate = models.CharField(max_length=250 , blank=True , null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "مستندات برون سازمانی "
        verbose_name_plural = "مستندات برون سازمانی"
    
 
 
      
    def __str__(self):
        return self.title 

class TextDataBase(models.Model):
    title = models.CharField(max_length=100)
    text  = models.TextField(null=True, blank=True ) 
     
    class Meta:
        verbose_name = "دیتابیس متن ها"
        verbose_name_plural = "دیتابیس متن ها"
    
    def __str__(self):
        return str(self.id)  + " " + str(self.title)


class BoolDataBase(models.Model):
    title   = models.CharField(max_length=100)
    boolean = models.BooleanField(null=True, blank=True ) 
     
    class Meta:
        verbose_name = "دیتابیس  bool"
        verbose_name_plural = "دیتابیس  bool"
    
    def __str__(self):
        return str(self.id)  + " " + str(self.title) + " " + str(self.boolean)


class ConfirmationDataBase(models.Model):
    CONFIRM_STATUS  = (('yes','بله'),('no','خیر') )
    title   = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile ,related_name='confirmationProfileMostanadatDakheli' , on_delete = models.CASCADE  ) 
    confirm = models.CharField(max_length=75, choices= CONFIRM_STATUS  )
    text  = models.TextField(null=True, blank=True ) 
    class Meta:
        verbose_name = "دیتابیس  کانفرم شدن"
        verbose_name_plural = "دیتابیس  کانفرم شدن"
    
    def __str__(self):
        return str(self.id)  + " " + str(self.title) 




class MostanadatDakheliChange(models.Model):
    PROBLEM_TYPE     = (('create','تدوین سند'),('edit','اصلاح سند') ,('delete' , 'حذف صند')  )
    
    problem          = models.CharField(max_length=75, choices= PROBLEM_TYPE ,null=True, blank=True ) 
    documentRelated = models.ForeignKey(MostanadatDakheli , blank=True, null=True, related_name="MostanadatDakheli" , on_delete = models.CASCADE )
    
   
    vahedRelated            = models.ForeignKey(Vahed , related_name='MostanadatDakheliChangeVahed' ,blank=True , null=True , on_delete = models.CASCADE)
    
    deadLine         = models.DateTimeField( null=True, blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "درخواست تغییر"
        verbose_name_plural = "درخواست تغییر"

    def __str__(self):
        return str(self.problem )
    def get_jalali_date(self):
        return date2jalali(self.deadLine)


def user_directory_path_mostanadatDakheli_change(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'mostanadatDakheli_change_document/{0}_{1}_{2}/{3}'.format(instance.reciver.user.id, instance.reciver.lastName , instance.reciver.firstName,filename)
def user_directory_path_correctiveAction(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'corrective_action_document/{0}_{1}_{2}/{3}'.format(instance.reciver.user.id, instance.reciver.lastName , instance.reciver.firstName,filename)
class MostanadatDakheliChangeActivityManager(models.Model):

    ACTIVITY_STATUS  = (('done','done'),('doing','doing'), ('completed' , 'completed') )
    ACTIVITY_LIST    = (('register','اطلاعات اولیه'),('barresiMafogh','تاییدیه اولیه مافوق'),('barresiKarshenas','بررسی کارشناس دفتر توسعه مدیریت و تحقیقات'), ('barresiModir','بررسی مدیر دفتر توسعه مدیریت و تحقیقات'), ('tadvinSanad','تدوین مدرک جدید') , ('isDelete' , 'آیا سند حذف میشود ؟') , ('newDoc' , 'بارگزاری و تدوین سند جدید') , ('editDoc' , 'ویرایش سند جدید') , ('reform' , 'اصلاح و تکمیل مدارک'))
    
    title            = models.CharField(max_length=250, blank=True , null=True  )
    question         = models.CharField(max_length=250, blank=True , null=True  )
    sender           = models.ForeignKey(Profile, null=True,  blank=True , related_name='SenderProfileMostanadatDakheliChange' , on_delete = models.CASCADE)
    reciver          = models.ForeignKey(Profile, null=True,  blank=True , related_name='ReciverProfileMostanadatDakheliChange' , on_delete = models.CASCADE)
    status           = models.CharField(max_length=75, choices= ACTIVITY_STATUS ,default='doing' )
    activity         = models.CharField(max_length=75, choices= ACTIVITY_LIST  )
    MostanadatDakheliChangeRelated  = models.ForeignKey(MostanadatDakheliChange , related_name='MostanadatDakheliRelated' , on_delete = models.CASCADE, null=True,  blank=True )
    texts            = models.ManyToManyField(TextDataBase ,related_name="textData"   )
    bools            = models.ManyToManyField(BoolDataBase ,related_name="BoolData"  )
    file             = models.FileField(upload_to=(user_directory_path_mostanadatDakheli_change) ,blank=True, null=True)
    startTiem        = models.DateTimeField( null=True, blank=True)
    deadLine         = models.DateTimeField( null=True, blank=True)
    previousActivity = models.ForeignKey('self' , null=True,  blank=True , related_name='PrActivityMostanadatDakheliChange' , on_delete = models.CASCADE)
    nextActivity     = models.ForeignKey('self' , null=True,  blank=True , related_name='NeActivityMostanadatDakheliChange' , on_delete = models.CASCADE)
    confirmations    = models.ForeignKey(ConfirmationDataBase ,related_name="confirmationData" , on_delete = models.CASCADE , null=True,  blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    def filename(self):
        return os.path.basename(self.file.name)
    class Meta:
        verbose_name = "مدیریت فعالیت های تغییر مستندات داخلی   "
        verbose_name_plural = "مدیریت فعالیت های تغییر مستندات داخلی   "
    
    def __str__(self):
        return str(self.id)  + " " + str(self.sender)
    
    def lastStep(self):
        last = self
        while(True):

            if(last.nextActivity != None):
               
                last = last.nextActivity
            else:
                return last
    def allActivityList(self):
        selected = self.firstStep()
        listActivity = []
        listActivity.append(selected)

        while(True):
            if(selected.nextActivity !=None):
                listActivity.append(selected.nextActivity)
                selected = selected.nextActivity
            else:
                break
        return listActivity
    def firstStep(self):
        first = self
        while(True):

            if(first.previousActivity != None):
            
                first = first.previousActivity
            else:
                return first

    def listActivity(self):
        listItem = []
        item = self
        while(True):
            if(item.previousActivity != None):
                print(self.nextActivity)
                listItem.append(item)
                item = item.previousActivity
            else:
                listItem.append(item)
                break


    def findStep(self , step):
        item = self
        while(True):
      
            if(item.activity == step):
                break
            else:
                if(item.previousActivity is not None):
                    item = item.previousActivity
                else:
                    item = None
                    break
        return (item)




class RecordDataBase(models.Model):
    PRIVACY_LIST    = (('internal' , 'داخلی') , ('secret' , 'محرمانه') )
    TYPE_LIST       = (('electronic' , 'الکترونیکی') , ('paper' , 'کاغذی') )
    title = models.CharField(max_length=100)
    recordCode = models.CharField(max_length=100)
    postKeeper = models.ForeignKey(TypePostSazmani , blank=True, null=True, related_name="postKeeper" , on_delete = models.CASCADE )
    vahedKeeper = models.ForeignKey(Vahed , blank=True, null=True, related_name="vahedKeeper" , on_delete = models.CASCADE )
    privacy     = models.CharField(max_length=75, choices= PRIVACY_LIST  )
    typeKeeping     = models.CharField(max_length=75, choices= TYPE_LIST  )
    determine      = models.TextField( null=True, blank=True)
    
    jariY   = models.IntegerField( null=True, blank=True)
    jariM   = models.IntegerField( null=True, blank=True)
    rakedY   = models.IntegerField( null=True, blank=True)
    rakedM   = models.IntegerField( null=True, blank=True)


    
    updated_at           = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        verbose_name = "لیست سوابق   "
        verbose_name_plural = " لیست سوابق "
      
    def __str__(self):
        return self.title 
    
    def get_jalali_date(self):
        return date2jalali(self.jari)
    
class RecordChange(models.Model):
    
    
    
    recordRelated = models.ForeignKey(RecordDataBase , blank=True, null=True, related_name="MostanadatDakheli" , on_delete = models.CASCADE )
    
   
    
    
    deadLine         = models.DateTimeField( null=True, blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "درخواست تغییر سابقه"
        verbose_name_plural = "درخواست تغییر سابقه"

    def __str__(self):
        return str(self.recordRelated )
    def get_jalali_date(self):
        return date2jalali(self.deadLine)


class RecordChangeActivityManager(models.Model):

    ACTIVITY_STATUS  = (('done','done'),('doing','doing'), ('completed' , 'completed') , ('delete' , 'delete'))
    ACTIVITY_LIST    = (('register','ثبت درخواست '),('barresiMafogh','تاییدیه اولیه مافوق'),('barresiKarshenas','بررسی کارشناس دفتر توسعه مدیریت و تحقیقات'), ('barresiModir','بررسی مدیر دفتر توسعه مدیریت و تحقیقات'), ('editKarshenas','اصلاح اطلاعات لیست کنترل سوابق') ,  )
    
    title            = models.CharField(max_length=250, blank=True , null=True  )
    question         = models.CharField(max_length=250, blank=True , null=True  )
    sender           = models.ForeignKey(Profile, null=True,  blank=True , related_name='SenderProfileRecordChange' , on_delete = models.CASCADE)
    reciver          = models.ForeignKey(Profile, null=True,  blank=True , related_name='ReciverProfileRecordChange' , on_delete = models.CASCADE)
    status           = models.CharField(max_length=75, choices= ACTIVITY_STATUS ,default='doing' )
    activity         = models.CharField(max_length=75, choices= ACTIVITY_LIST  )
    RecordChangeRelated  = models.ForeignKey(RecordDataBase , related_name='RecordChangeRelated' , on_delete = models.CASCADE, null=True,  blank=True )
    texts            = models.ManyToManyField(TextDataBase ,related_name="RecordTextData"   )
    bools            = models.ManyToManyField(BoolDataBase ,related_name="RecordBoolData"  )
    file             = models.FileField(upload_to=(user_directory_path_mostanadatDakheli_change) ,blank=True, null=True)
    startTime        = models.DateTimeField( null=True, blank=True)
    deadLine         = models.DateTimeField( null=True, blank=True)
    previousActivity = models.ForeignKey('self' , null=True,  blank=True , related_name='PrActivityMostanadatDakheliChange' , on_delete = models.CASCADE)
    nextActivity     = models.ForeignKey('self' , null=True,  blank=True , related_name='NeActivityMostanadatDakheliChange' , on_delete = models.CASCADE)
    confirmations    = models.ForeignKey(ConfirmationDataBase ,related_name="confirmationRecordData" , on_delete = models.CASCADE , null=True,  blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    def filename(self):
        return os.path.basename(self.file.name)
    class Meta:
        verbose_name = "مدیریت فعالیت های درخواست اصلاح سوابق"
        verbose_name_plural = "مدیریت فعالیت های درخواست اصلاح سوابق"
    
    def __str__(self):
        return str(self.id)  + " " + str(self.sender)
    
    def lastStep(self):
        last = self
        while(True):

            if(last.nextActivity != None):
               
                last = last.nextActivity
            else:
                return last
    def allActivityList(self):
        selected = self.firstStep()
        listActivity = []
        listActivity.append(selected)

        while(True):
            if(selected.nextActivity !=None):
                listActivity.append(selected.nextActivity)
                selected = selected.nextActivity
            else:
                break
        return listActivity
    def firstStep(self):
        first = self
        while(True):

            if(first.previousActivity != None):
            
                first = first.previousActivity
            else:
                return first

    def listActivity(self):
        listItem = []
        item = self
        while(True):
            if(item.previousActivity != None):
                print(self.nextActivity)
                listItem.append(item)
                item = item.previousActivity
            else:
                listItem.append(item)
                break


    def findStep(self , step):
        item = self
        while(True):
      
            if(item.activity == step):
                break
            else:
                if(item.previousActivity is not None):
                    item = item.previousActivity
                else:
                    item = None
                    break
        return (item)

