from django.db import models
from organization_app.models import Vahed
from standardTable_app.models import Standard
from profile_app.models import Profile
from jalali_date import date2jalali 
# Create your models here.
class CorrectiveAction(models.Model):
    PROBLEM_TYPE     = (('correctiveAction','اقدام اصلاحی'),('Correction','درخواست اصلاح')   )
    SOURCE_TYPE     = (('MomayeziDakheli','ممیزی داخلی '),('risk','مدیریت ریسک ') , ('پایش و اندازه گیری فرآیند' , 'پایش و اندازه گیری فرآیند') , ('پایش و شناسایی تخلفات' , 'پایش و شناسایی تخلفات'), ('ممیزی خارجی' , 'ممیزی خارجی'), ('بازنگری و مدیریت' , 'بازنگری و مدیریت'), ('مدیریت تغییر' , 'مدیریت تغییر')   )
    problem          = models.CharField(max_length=75, choices= PROBLEM_TYPE ,null=True, blank=True ) 
    demandantVahed   = models.ForeignKey(Vahed , related_name="demandantVahed" , on_delete = models.CASCADE )
    demandantId      = models.CharField(max_length=250  )
    standardRelated  = models.ForeignKey(Standard , related_name="standardRelatedCorrective",blank=True , null=True , on_delete=models.CASCADE)
    source           = models.CharField(max_length=75, choices= SOURCE_TYPE ,null=True, blank=True ) 
    vahed            = models.ForeignKey(Vahed , related_name='CorrectiveActionVahed' ,blank=True , null=True , on_delete = models.CASCADE)
    owner            = models.ForeignKey(Profile , related_name='profileOwnerCorrectiveAction' ,blank=True , null=True , on_delete = models.CASCADE)
    deadLine         = models.DateTimeField( null=True, blank=True)
    effective        = models.BooleanField(blank=True , null=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "اقدام اصلاحی"
        verbose_name_plural = "اقدام اصلاحی"

    def __str__(self):
        return self.demandantId 
    def get_jalali_date(self):
        return date2jalali(self.deadLine)
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
    profile = models.ForeignKey(Profile ,related_name='confirmationProfile' , on_delete = models.CASCADE  ) 
    confirm = models.CharField(max_length=75, choices= CONFIRM_STATUS  )
    text  = models.TextField(null=True, blank=True ) 
    class Meta:
        verbose_name = "دیتابیس  کانفرم شدن"
        verbose_name_plural = "دیتابیس  کانفرم شدن"
    
    def __str__(self):
        return str(self.id)  + " " + str(self.title) 
    
def user_directory_path_correctiveAction(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'corrective_action_document/{0}_{1}_{2}/{3}'.format(instance.reciver.user.id, instance.reciver.lastName , instance.reciver.firstName,filename)
class CorrectiveActionActivityManager(models.Model):
    ACTIVITY_STATUS  = (('done','done'),('doing','doing'), ('completed' , 'completed') )
    ACTIVITY_LIST    = (('description','شرح مسئله/ درخواست'),('barresiMafogh','بررسی درخواست توسط مافوق' ),('executiveUnit','تعیین واحد مجری ') , ('register' , 'ثبت اطلاعات پایه'),('barresiModir','بررسی درخواست توسط مدیر') ,('cause','علت و ریشه ') ,('barresiMoaven','بررسی درخواست توسط معاون') , ('definitionCorrectiveaAtion','تعریف اقدام اصلاحی') ,('ejraNatije','ثبت نتیجه اقدام') ,('confirmRiportMotevali' , 'تایید گزارش  توسط واحد متولی'),('confirmRiportModir' , 'تایید گزارش  توسط مدیر دفتر توسعه مدیریت و تحقیقات') , ('effective' , 'اثربخشی'))
    sender           = models.ForeignKey(Profile, null=True,  blank=True , related_name='SenderProfileCorrective' , on_delete = models.CASCADE)
    reciver          = models.ForeignKey(Profile, null=True,  blank=True , related_name='ReciverProfileCorrective' , on_delete = models.CASCADE)
    status           = models.CharField(max_length=75, choices= ACTIVITY_STATUS ,default='doing' )
    activity         = models.CharField(max_length=75, choices= ACTIVITY_LIST  )
    CorrectiveActionRelated  = models.ForeignKey(CorrectiveAction , related_name='CorrectiveActionRelated' , on_delete = models.CASCADE, null=True,  blank=True )
    texts            = models.ManyToManyField(TextDataBase ,related_name="textData" ,  )
    bools            = models.ManyToManyField(BoolDataBase ,related_name="BoolData" , )
    file             = models.FileField(upload_to=(user_directory_path_correctiveAction) ,blank=True, null=True)
    startTiem        = models.DateTimeField( null=True, blank=True)
    deadLine         = models.DateTimeField( null=True, blank=True)
    previousActivity = models.ForeignKey('self' , null=True,  blank=True , related_name='PrActivityCorrectiveAction' , on_delete = models.CASCADE)
    nextActivity     = models.ForeignKey('self' , null=True,  blank=True , related_name='NeActivityCorrectiveAction' , on_delete = models.CASCADE)
    confirmations    = models.ForeignKey(ConfirmationDataBase ,related_name="confirmationData" , on_delete = models.CASCADE , null=True,  blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "مدیریت فعالیت های اقدام اصلاحی   "
        verbose_name_plural = "مدیریت فعالیت های اقدام اصلاحی   "
    
    def __str__(self):
        return str(self.id)  + " " + str(self.sender)
    
    def lastStep(self):
        last = self
        while(True):

            if(last.nextActivity != None):
               
                last = last.nextActivity
            else:
                return last
            
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
               
                listItem.append(item)
                item = item.previousActivity
            else:
                listItem.append(item)
                break
        New_list = listItem.copy()
        New_list.reverse()
        
      
        return New_list
            
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