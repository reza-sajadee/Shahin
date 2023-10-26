from django.db import models

from organization_app.models import Vahed , JobBank
from standardTable_app.models import Standard
from profile_app.models import Profile
from process_app.models import Process
from jalali_date import date2jalali 
# Create your models here.
from performanceIndex_app.utils import gregorian_to_jalali
from datetime import datetime
class PerformanceSettings(models.Model):
    startPeriod = models.IntegerField(default=1)
    endPeriod   = models.IntegerField(default=5)

    
     
    class Meta:
        verbose_name = "نمظیمات شاخص"
        verbose_name_plural = "نمظیمات شاخص"
    
    def __str__(self):
        return str(self.id) 
 

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
    profile = models.ForeignKey(Profile ,related_name='PerformanceIndexConfirmProfile' , on_delete = models.CASCADE  ) 
    confirm = models.CharField(max_length=75, choices= CONFIRM_STATUS  )
    text  = models.TextField(null=True, blank=True ) 
    class Meta:
        verbose_name = "دیتابیس  کانفرم شدن"
        verbose_name_plural = "دیتابیس  کانفرم شدن"
    
    def __str__(self):
        return str(self.id)  + " " + str(self.title) 
    
class SubjectPerformanceIndex(models.Model):
    title            = models.CharField(max_length=100)

    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "سرفصل عملکردی"
        verbose_name_plural = "سرفصل عملکردی"

class TopicPerformanceIndex(models.Model):
    title            = models.CharField(max_length=100)
    subjectRelated   = models.ForeignKey(SubjectPerformanceIndex ,related_name='topicSubjectRelated' , on_delete = models.CASCADE  )

    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = "محور عملکردی"
        verbose_name_plural = "محور عملکردی"
def user_directory_path_performance_index(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'performance_index_document/'
class PerformanceIndex(models.Model):
    INDEX_TYPE              = (('Effectiveness','اثربخشی'),('Performance','کارایی')  )
    title                      = models.CharField(max_length=100)  
    codePerformanceIndex       = models.CharField(max_length=100)
    processRelated             = models.ForeignKey(Process , related_name="ProcessRelatedPerformanceIndex",blank=True , null=True , on_delete=models.CASCADE) 
    #goalRelated                
    indexType                  = models.CharField(max_length=100 , choices= INDEX_TYPE)
    reference                  = models.CharField(max_length=100)
    standardRelated            = models.ForeignKey(Standard , related_name="standardRelatedPerformanceIndex",blank=True , null=True , on_delete=models.CASCADE) 
    stackHolder                = models.CharField(max_length=100)
    document                   = models.FileField(upload_to=('performance_index_document/') ,blank=True, null=True)


    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = "معیار عملکردی"
        verbose_name_plural = "معیار عملکردی"

class VariableDataBase(models.Model):
    title            = models.CharField(max_length=100 ,unique=True)
    description      = models.TextField(null=True, blank=True ) 
    code             = models.CharField(max_length=100)
    responsible      =  models.ForeignKey(JobBank , related_name='responsibleProfileVariablePerformanceFormula' ,blank=True , null=True , on_delete = models.CASCADE , verbose_name='مسئول وارد کردن ')
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
        
    class Meta:

        verbose_name = "متغیر"
        verbose_name_plural = "متغیر"


class PerformanceFormula(models.Model):
    CYCLE_TYPE               = (('monthly','ماهانه'),('seasonal','سه ماهه'),('semiAnnualy','شش ماهه') , ('annualy','سالانه')    )
    CONDITION_TYPE              = (('smaller','کوچکتر'),('bigger','بزرگتر'),('equal','برابر') ,  ('beetween' , 'بین') )
    performanceIndexRelated  = models.ForeignKey(PerformanceIndex , related_name='performanceRelatedFormula' ,blank=True , null=True , on_delete = models.CASCADE )
    acceptableCondition      = models.CharField(max_length=75, choices= CONDITION_TYPE ,null=True, blank=True ) 
    acceptableCriteria       = models.FloatField(blank=True , null=True)
    acceptableCriteriaSecond = models.FloatField(blank=True , null=True)
    cycle                    = models.CharField(max_length=75, choices= CYCLE_TYPE ,null=True, blank=True ) 
    responsible              = models.ForeignKey(JobBank , related_name='responsibleProfilePerformanceFormula' ,blank=True , null=True , on_delete = models.CASCADE ,verbose_name='مسئول پایش شاخص')
    metric                   = models.CharField(max_length=100)
    PerformanceFormula       = models.CharField(max_length=100 ,blank=True , null=True)
    variablesRelated         = models.ManyToManyField(VariableDataBase)
    created_at               = models.DateTimeField(auto_now_add=True)
    updated_at               = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
        
    class Meta:
        verbose_name = "فرمول شاخص عملکردی"
        verbose_name_plural = "فرمول شاخص عملکردی"

    def get_all_varibels(self):
        return VariableDataBase.objects.all()


class PerformanceIndexActivityManager(models.Model):
    ACTIVITY_STATUS  = (('done','done'),('doing','doing'), ('completed' , 'completed') )
    ACTIVITY_LIST    = (('insert' , 'ورود اطلاعات'),)
    
    reciver          = models.ForeignKey(Profile, null=True,  blank=True , related_name='ReciverProfilePErformanceIndex' , on_delete = models.CASCADE)
    status           = models.CharField(max_length=75, choices= ACTIVITY_STATUS ,default='doing' )
    activity         = models.CharField(max_length=75, choices= ACTIVITY_LIST  ,default='insert' )
    
    texts            = models.TextField(blank=True , null=True)

   # file             = models.FileField(upload_to=(user_directory_path_correctiveAction) ,blank=True, null=True)
    startTime        = models.DateField( null=True, blank=True)
    deadLine         = models.DateField( null=True, blank=True)
    variableRelated  = models.ForeignKey(VariableDataBase , blank=True , null=True , related_name='variableRelatedPerformanceIndexActivityManager' , on_delete = models.CASCADE)
    previousActivity = models.ForeignKey('self' , null=True,  blank=True , related_name='PrActivityPerformanceIndex' , on_delete = models.CASCADE)
    nextActivity     = models.ForeignKey('self' , null=True,  blank=True , related_name='NeActivityPerformanceIndex' , on_delete = models.CASCADE)
   
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "مدیریت فعالیت های شاخص عملکردی    "
        verbose_name_plural = "مدیریت فعالیت های شاخص عملکردی    "
    def getResidual(self):
      
        r = self.deadLine - datetime.today().date()
      
        return r.days
    
    def getMonth(self):
       
        return gregorian_to_jalali(self.startTime.year , self.startTime.month , self.startTime.day)[1]
    def __str__(self):
        return str(self.id)  
    
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