from django.db import models
from organization_app.models import JobBank
from goal_app.models import Objective
from profile_app.models import Profile
from datetime import datetime
# Create your models here.
class ProjectProfile(models.Model):
    RESOURCE_STATUS  = (('Objective','هدف خرد'),('Other' , 'سایر'))
    STATUS = (('defination','تعریف پروژه'),('executive', 'اجرای پروژه'))
    title = models.CharField(max_length=250, verbose_name='عنوان پروژه', blank=True , null=True) 
    accountable     = models.ForeignKey(JobBank , blank=True, null=True, related_name="responsibleProjectProfile" , on_delete = models.CASCADE )
    description      = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    targetRequired   = models.TextField(blank=True, null=True, verbose_name='هدف مورد نظر')
    capitalEstimate = models.TextField(blank=True, null=True, verbose_name='بودجه مدنظر')
    diurationEsimate = models.TextField(blank=True, null=True, verbose_name='زمان مورد نظر')
    sourceProject = models.CharField(max_length=250,choices=RESOURCE_STATUS , default='Objective', verbose_name='منشا', blank=True , null=True)  
    sourceId = models.IntegerField(blank=True , null=True , verbose_name='آی دی مرجع')
    status  = models.CharField(max_length=250,choices=STATUS , default='defination', verbose_name='وضعیت', blank=True , null=True)  
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    
class Project(models.Model):
    STATUS = (('defination','تعریف'),('executive', 'اجرا'))
    TREND_STATUS  = (('upTrend','روند افزایشی'),('downTrend','روند کاهشی'),('side','روند ثابت') )
    RESOURCE_STATUS  = (('Objective','هدف خرد'),)
    DEPENDENCIES_STATUS  = (('predecessor','پیش نیاز '),('successor','پس نیاز'),('corequisite','همنیاز') , ('independ','بی ارتباط'))
    profileProjectRelated = models.ForeignKey(ProjectProfile, blank=True, null=True, related_name='profileProjectRelatedProject' , on_delete=models.CASCADE)
    code = models.CharField(max_length=250, verbose_name='کد' , blank=True , null=True)
    title = models.CharField(max_length=250, verbose_name='عنوان پروژه', blank=True , null=True) 
    responsible = models.ForeignKey(JobBank , blank=True, null=True, related_name="responsibleProject" , on_delete = models.CASCADE )
    startTime = models.DateTimeField( null=True, blank=True) 
    deadLine = models.DateTimeField( null=True, blank=True)
    index = models.CharField(max_length=250, verbose_name='شاخص', blank=True , null=True)
    currentSituation = models.CharField(max_length=250, verbose_name='وضعیت موجود', blank=True , null=True) 
    target = models.CharField(max_length=250, verbose_name='معیار', blank=True , null=True) 
    resourceProject = models.CharField(max_length=250,choices=RESOURCE_STATUS , default='Objective', verbose_name='منشا', blank=True , null=True)  
    resourceId = models.IntegerField(blank=True , null=True , verbose_name='آی دی مرجع')
    description = models.TextField(blank=True, null=True, verbose_name='منشا')
    controller  = models.ForeignKey(JobBank , blank=True, null=True, related_name="controllerProject" , on_delete = models.CASCADE )
    accountable     = models.ForeignKey(JobBank , blank=True, null=True, related_name="accountableProject" , on_delete = models.CASCADE )
    taskDependencies  = models.CharField(max_length=250,choices=DEPENDENCIES_STATUS , default='Objective', verbose_name='وابستگی تسک', blank=True , null=True)  
    status  = models.CharField(max_length=250,choices=STATUS , default='defination', verbose_name='وابستگی تسک', blank=True , null=True)  
    previousProject = models.ForeignKey('self' , null=True,  blank=True , related_name='PrProject' , on_delete = models.CASCADE)
    nextProject     = models.ManyToManyField('self',null=True , blank=True , related_name='NeProject', symmetrical=False)
    
    
 
   
    def level(self):
        if(self.previousProject == None):
            return 1
        else:
            return 2
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه"
    def __str__(self):
        return str(self.id )
    
class Task(models.Model):
    TREND_STATUS  = (('upTrend','روند افزایشی'),('downTrend','روند کاهشی'),('side','روند ثابت') )
    title = models.CharField(max_length=250, verbose_name='عنوان اقدام', blank=True , null=True) 
    responsible = models.ForeignKey(JobBank , blank=True, null=True, related_name="responsibleTask" , on_delete = models.CASCADE )
    startTime             = models.DateTimeField( null=True, blank=True) 
    deadLine             = models.DateTimeField( null=True, blank=True)
    index = models.CharField(max_length=250, verbose_name='شاخص', blank=True , null=True)
    controller    = models.ForeignKey(JobBank , blank=True, null=True, related_name="controllerTask" , on_delete = models.CASCADE )
    requirementResource = models.CharField(max_length=250, verbose_name='شاخص', blank=True , null=True)
    financialResource = models.CharField(max_length=250, verbose_name='شاخص', blank=True , null=True)
    timeResource  = models.CharField(max_length=250, verbose_name='شاخص', blank=True , null=True)
    weightOfRequirement  = models.FloatField(blank=True , null=True)
    weightOfFinancial  = models.FloatField(blank=True , null=True)
    weightOfTime = models.FloatField(blank=True , null=True)
    currentSituation = models.CharField(max_length=250, verbose_name='وضعیت موجود', blank=True , null=True) 
    target = models.CharField(max_length=250, verbose_name='معیار', blank=True , null=True) 
    
    
    projectRelated = models.ForeignKey(Project , null=True , blank=True , related_name='projectRelatedTask' , on_delete = models.CASCADE)
    previousProject = models.ForeignKey('self' , null=True,  blank=True , related_name='PrProject' , on_delete = models.CASCADE)
    nextProject     = models.ForeignKey('self' , null=True,  blank=True , related_name='NeProject' , on_delete = models.CASCADE)
    
    
    
   
    
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "اقدام"
        verbose_name_plural = "اقدام"
    def __str__(self):
        return str(self.id )
    
    
    def percentage(value):
        return '{0:.2%}'.format(value)
    
    

class PlanProfile(models.Model):
    RESOURCE_STATUS  = (('corrective','اقدام اصلاحی'),('risk' , 'ریسک'),('meeting' , 'مصوبات جلسه'),('suggestion' , 'نظام پیشنهادی'),('goal' , 'هدف'),('other' , 'سایر'))
    STATUS_STATUS = (('complate','اتمام شده'),('pending' , 'در انتظار انجام'),('doing' , 'در حال انجام'))
    title = models.CharField(max_length=250, verbose_name='عنوان برنامه اجرایی', blank=True , null=True) 
    accountable     = models.ForeignKey(JobBank , blank=True, null=True, related_name="accountablePlanProfile" , on_delete = models.CASCADE )
    responsible = models.ForeignKey(JobBank , blank=True, null=True, related_name="responsiblePlanProfile" , on_delete = models.CASCADE )
    description      = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    sourcePlan = models.CharField(max_length=250,choices=RESOURCE_STATUS , default='personal', verbose_name='منشا', blank=True , null=True)  
    startTiem        = models.DateTimeField( null=True, blank=True)
    deadLine         = models.DateTimeField( null=True, blank=True)
    status  = models.CharField(max_length=250,choices=STATUS_STATUS , default='doing', verbose_name='وضعیت', blank=True , null=True)  
    
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

class Action(models.Model):
    STATUS_STATUS = (('complate','اتمام شده'),('doing' , 'در حال انجام'),('done' , 'انجام شد'))
    COLOR_STATUS = (('0','--accent-color:#41516C'),('1' , '--accent-color:#FBCA3E'),('2' , '--accent-color:#E24A68'),('3' , '--accent-color:#1B5F8C'),('4' , '--accent-color:#4CADAD'))
    planProfileRelated = models.ForeignKey(PlanProfile, blank=True, null=True, related_name='planProfileRelated' , on_delete=models.CASCADE)
    responsible = models.ForeignKey(JobBank , blank=True, null=True, related_name="responsibleAction" , on_delete = models.CASCADE )
    title = models.CharField(max_length=250, verbose_name='عنوان برنامه اجرایی', blank=True , null=True) 
    
    description      = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    startTiem        = models.DateTimeField( null=True, blank=True)
    deadLine         = models.DateTimeField( null=True, blank=True)
    status  = models.CharField(max_length=250,choices=STATUS_STATUS , default='doing', verbose_name='وضعیت', blank=True , null=True)  
    color =  models.CharField(max_length=250,choices=COLOR_STATUS , default='1', verbose_name='رنگ', blank=True , null=True)  
    progress = models.IntegerField(default=0 )
    weight =  models.IntegerField( null=True, blank=True, default=0 )

    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def get_status_today(self):
        x = self.deadLine.date()
        y = datetime.now().date()
        if self.status == 'done':
            return 'success'
        if x < y:

            return 'danger'
        else:
            return 'warning'
    def max_weight(self):
        allAction = Action.objects.filter(planProfileRelated = self.planProfileRelated)
        maxWeight = 100
        for action in allAction:
            maxWeight = maxWeight - action.weight
        return maxWeight
    def planed_progress(self):
        allDayes = self.deadLine.date() - self.startTiem.date()
        passedDays = datetime.now().date() - self.startTiem.date()
        x = int((passedDays / allDayes) * 100)
        if(x < 0):
            x = 0
        if(x > 100):
            x = 100
        return x