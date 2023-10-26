from django.db import models

from profile_app.models import Profile
# Create your models here.
from django.db.models.fields.related import ForeignKey , ManyToManyField
from committee_app.models import Committee
from organization_app.models import Vahed
from process_app.models import Hoze , Group , Process



class QuestionDaste(models.Model):
    
    title            = models.CharField(max_length=250 )

    
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "دسته بندی سوال "
        verbose_name_plural = "دسته بندی سوال "
    
    def __str__(self):
        return self.title 

class RiskTopic(models.Model):
    
    title            = models.CharField(max_length=250 )
    vahed            = models.ForeignKey(Vahed , related_name='vahedMortabetRisk' , on_delete = models.CASCADE)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "سرفصل ریسک"
        verbose_name_plural = "سرفصل ریسک"
    
    def __str__(self):
        return self.title 


class RiskProfile(models.Model):
    STEP_LIST    = (('1','تعریف تیم ها '),('2','شناسایی ریسک'),('2','بررسی ریسک های شناسایی شده'),('3','ارزیابی ریسک'),('4','پایان'), )
    step           = models.CharField(max_length=75, choices= STEP_LIST ,default='1' )
    title            = models.CharField(max_length=250 )
    committeeRisk    = models.ForeignKey(Committee , related_name="committeeRisk" , on_delete = models.CASCADE )

    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "پروفایل ریسک "
        verbose_name_plural = "پروفایل ریسک "
    
    def __str__(self):
        return self.title 





class RiskTeam(models.Model):
    
    title            = models.CharField(max_length=250  )
    riskProfile      = models.ForeignKey(RiskProfile , blank=True, null=True, related_name="riskProfileTeamRelated" , on_delete = models.CASCADE )
    memberProfile    = models.ManyToManyField(Profile)
    riskTopic        = models.ForeignKey(RiskTopic , related_name="RiskTeamTopic" , blank=True, null=True , on_delete = models.CASCADE)
    hoze             = models.ManyToManyField(Hoze ,related_name="RiskTeamHoze")
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "تیم ارزشیابی ریسک "
        verbose_name_plural = "تیم ارزشیابی ریسک  "
    
    def __str__(self):
        return self.title
    
 

class RiskActivityManager(models.Model):
    ACTIVITY_STATUS  = (('done','به اتمام رسیده'),('doing','درحال انجام'),('doNot' , 'انجام نشد') )
    ACTIVITY_LIST    = (('team','تعریف تیم ها '),('identification','شناسایی ریسک'),('Conclusion','جمع بندی ریسک'),('measurement','ارزیابی'),('evaluation','ارزیابی ریسک') )
    sender           = models.ForeignKey(Profile, null=True,  blank=True , related_name='SenderProfile' , on_delete = models.CASCADE)
    reciver          = models.ForeignKey(Profile, null=True,  blank=True , related_name='ReciverProfile' , on_delete = models.CASCADE)
    status           = models.CharField(max_length=75, choices= ACTIVITY_STATUS ,default='doing' )
    activity         = models.CharField(max_length=75, choices= ACTIVITY_LIST  )
    team             = models.ForeignKey(RiskTeam, null=True,  blank=True , related_name='RiskTeamActivityManager' , on_delete = models.CASCADE)
    riskTopic        = models.ForeignKey(RiskTopic, null=True,  blank=True ,  related_name="activityRiskTopic" , on_delete = models.CASCADE)
    hoze             = models.ForeignKey(Hoze , null=True,  blank=True ,related_name="activityHoze", on_delete = models.CASCADE)
    previousActivity = models.ForeignKey('self' , null=True,  blank=True , related_name='PrActivity' , on_delete = models.CASCADE)
    nextActivity     = models.ForeignKey('self' , null=True,  blank=True , related_name='NeActivity' , on_delete = models.CASCADE)
    riskProfile      = models.ForeignKey(RiskProfile , related_name="riskProfileActivity" , on_delete=models.CASCADE)
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "مدیریت فعالیت های ریسک   "
        verbose_name_plural = "مدیریت فعالیت های ریسک   "
    
    def __str__(self):
        return str(self.id) + "-" + str(self.team ) + " " + str(self.sender)
    
    
    
   
class RiskIdentification(models.Model):
    ACTIVITY_LIST    = (('identification','identification'),('measurement','measurement'),('Conclusion','Conclusion'),('evaluation','evaluation') )
    riskFailureModes = models.CharField(verbose_name = 'عنوان ریسک' ,max_length=250 )
    riskCauses       = models.TextField(verbose_name = 'علل بروز خطا' ,max_length=250 )
    riskEffects      = models.TextField(verbose_name = 'اثرات بروز خطا' ,max_length=250 )
    currentAction    = models.TextField(verbose_name = 'کنترل های فعلی' )
    team             = models.ForeignKey(RiskTeam,verbose_name = 'تیم'   , related_name='TeamRiskIdentification' , on_delete = models.CASCADE)    
    recommender      = models.ForeignKey(Profile ,verbose_name = 'پیشنهاد دهنده'  , related_name='RecommenderRiskIdentification' , on_delete = models.CASCADE)    
    process          = models.ForeignKey(Process ,verbose_name = 'فرآیند'  , related_name='ProcessRiskIdentification' , on_delete = models.CASCADE)    
    group            = models.ForeignKey(Group ,verbose_name = 'گروه فرآیندی ' , related_name='ProcessGroupRiskIdentification', on_delete = models.CASCADE)    
    activity         = models.ForeignKey(RiskActivityManager ,verbose_name = 'قعالیت مرتبط' , related_name='RiskActivityIdentification',blank=True, null=True , on_delete = models.CASCADE)    
    status           = models.CharField(max_length=75, choices= ACTIVITY_LIST ,default='identification' )
    hoze             = models.ForeignKey(Hoze  ,related_name="riskHoze", on_delete = models.CASCADE) 
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "شناسایی ریسک   "
        verbose_name_plural = " شناسایی ریسک  "
    
    def __str__(self):
        return self.riskFailureModes 

  

class RiskIdentificationSelecting(RiskIdentification):
    riskIdentifications        = models.ManyToManyField(RiskIdentification , related_name="riskIdentifications" )
    class Meta:
        verbose_name = "انتخاب ریسک های شناسایی شده   "
        verbose_name_plural = "انتخاب ریسک های شناسایی شده"
        
        
class RiskMeasurement(models.Model):
    
    riskSeverity        = models.DecimalField(verbose_name = 'شدت اثر'  ,max_digits=10, decimal_places=0 ,blank = True ,null = True)
    riskOccurrence      = models.DecimalField(verbose_name = 'احتمال وقوع'  ,max_digits=10, decimal_places=0 ,blank = True ,null = True)
    riskDetection       = models.DecimalField(verbose_name = 'قابلیت کشف'  ,max_digits=10, decimal_places=0 ,blank = True ,null = True)
    
    riskIdentificated= models.ForeignKey(RiskIdentification,verbose_name = 'ریسک شناسایی شده' , related_name='RiskIdentificated',blank=True, null=True , on_delete = models.CASCADE)   
    activity         = models.ForeignKey(RiskActivityManager ,verbose_name = 'قعالیت مرتبط' , related_name='RiskActivityMeasurement',blank=True, null=True , on_delete = models.CASCADE)    
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "ارزیابی ریسک"
        verbose_name_plural = "ارزیابی ریسک"
    
    def __str__(self):
        return str(self.riskIdentificated.process.title)
    
    

class RiskProcessRelated(models.Model):
    
    
    riskProfile      = models.ForeignKey(RiskProfile , related_name="riskProfile" , on_delete=models.CASCADE)
    title            = models.CharField(max_length=250)
    
    
    
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "فرآیند مرتبط با ریسک"
        verbose_name_plural = "فرآیند مرتبط با ریسک"
    
    def __str__(self):
        
        return str(self.title)
    
    
    

class RiskProcess(models.Model):
    
    riskProfileRelated = models.ForeignKey(RiskProfile , related_name='riskProfileRelatedProcess',default=5, on_delete = models.CASCADE )
        
    riskMeasurement        = models.ForeignKey(RiskMeasurement,verbose_name = 'ریسک اریابی شده' , on_delete=models.CASCADE ,blank = True, null=True)
    process                = models.ForeignKey(Process,verbose_name = 'فرآیند' , on_delete=models.CASCADE)
    avgRiskSeverity        = models.FloatField(verbose_name = 'میانگین شدت اثر'  ,blank = True ,null = True)
    avgRiskOccurrence      = models.FloatField(verbose_name = 'میانگین احتمال وقوع'  ,blank = True ,null = True)
    avgRiskDetection       = models.FloatField(verbose_name = 'میانگین قابلیت کشف'  ,blank = True ,null = True)
    rpn                    = models.FloatField(verbose_name = 'اولویت ریسک'  ,blank = True ,null = True)
    rpnAdjusted            = models.FloatField(verbose_name = 'اولویت ریسک تعدیل شده'  ,blank = True ,null = True)
    
    
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "ریسک فرآیند"
        verbose_name_plural = "ریسک فرآیند"
    
    def __str__(self):
        
        return str(self.process)


class extraData(models.Model):
    
    
    RiskProcessRelated     = models.ForeignKey(RiskProcess,verbose_name = 'اطلاعات اضاقی' , on_delete=models.CASCADE , related_name='riskProcessRelatedExtra')
    control                 = models.TextField(null=True , blank=True)
    eghdam                  = models.TextField(null=True , blank=True)
    masol                   = models.TextField(null=True , blank=True)
    tarikh                  = models.TextField(null=True , blank=True)
    natije                  = models.TextField(null=True , blank=True)
    newRisk                 = models.TextField(null=True , blank=True)
    tarif                   = models.TextField(null=True , blank=True)
    dec                 = models.TextField(null=True , blank=True)
    
    
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = " اطلاعات اضافی ریسک"
        verbose_name_plural = " اطلاعات اضافی ریسک"
    
    def __str__(self):
        
        return str(self.id)
