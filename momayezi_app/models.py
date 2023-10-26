from django.db import models
from django.db.models.fields.related import ForeignKey , ManyToManyField

from organization_app.models import Vahed
from organization_app.models import TypePostSazmani
from standardTable_app.models import Standard
from process_app.models import Process 
from jalali_date import date2jalali 
from profile_app.models import Profile
from standardTable_app.models import RequirementStandards

class TypeMomayezi(models.Model):
    STEP_LIST    = (('1','تعریف تیم') ,('2','برنامه زمانی'),('3','چک لیست سوال'),('4','چک لیست') , ('5' , 'گزارش') , ('6' , 'پایان'))
    title = models.CharField(max_length=100)
    
    modir = models.ForeignKey(Profile , related_name="modirMomayezi" , on_delete=models.CASCADE)
     
    step           = models.CharField(max_length=75, choices= STEP_LIST ,default='1' )
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title 

  
    
class MomayeziTeam(models.Model):
    
    title            = models.CharField(max_length=250  )
    typeMomayeziRelated     = models.ForeignKey(TypeMomayezi , related_name="typeMomayeziTeam" , on_delete=models.CASCADE)
    memberMomayezi   = models.ManyToManyField(Profile , related_name="memberMomayeziTeam")
    standardRelated  = models.ForeignKey(Standard , related_name="standardRelated",blank=True , null=True , on_delete=models.CASCADE)
    vahedMomayezi    = models.ManyToManyField(Vahed , related_name="vahedMomayeziTeam"  )
    sarMomayez       = models.ForeignKey(Profile , related_name="sarMomayez",blank=True , null=True , on_delete=models.CASCADE)
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "تیم ممیزی"
        verbose_name_plural = "تیم ممیزی"
    
    def __str__(self):
        return str(self.title)

class CalenderMomayezi(models.Model):
    
    
    dateMomayezi   = models.DateTimeField( null=True, blank=True)
    vahedMomayezi  = models.ForeignKey(Vahed , blank=True, null=True, related_name="vahedMomayezi" , on_delete = models.CASCADE )
    timeStart      = models.TimeField( null=True, blank=True)
    timeDuration   = models.TimeField( null=True, blank=True)
    teamMomayezi   = models.ForeignKey( MomayeziTeam,null=True,  related_name="MomayeziTeam" , on_delete=models.CASCADE)
    systemMomayezi = models.ForeignKey(Standard ,default=1  , related_name="systemMomayezi" , on_delete=models.CASCADE)
    bandMomayezi   = models.ManyToManyField(RequirementStandards ,related_name="bandMomayeziCalender" )
    
    

    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "زمانبندی ممیزی"
        verbose_name_plural = "زمانبندی ممیزی"
        
    def __str__(self):
        return str(self.id)  
    def get_jalali_date(self):
        return date2jalali(self.dateMomayezi)
    

class NoghatGhovat(models.Model):
    title = models.CharField(max_length=250)
    typeMomayeziRelated = models.ForeignKey(TypeMomayezi  , related_name='typeMomayeziRelatedGovat' ,on_delete=models.CASCADE)
    teamGhovat           = models.ForeignKey(MomayeziTeam , blank=True , null=True , related_name="teamGhovat" , on_delete = models.CASCADE )
    calenderGhovat       = models.ForeignKey(CalenderMomayezi , blank=True , null=True , related_name="calenderGhovat" , on_delete = models.CASCADE )
    vahedGhovat          = models.ForeignKey(Vahed , blank=True , null=True , related_name="vahedGhovat" , on_delete = models.CASCADE )
    systemGhovat         = models.ForeignKey(Standard , blank=True , null=True , related_name="systemGhovat" , on_delete = models.CASCADE )
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title 
    

class ForsatBehbod(models.Model):
    title = models.CharField(max_length=250)
    typeMomayeziRelated = models.ForeignKey(TypeMomayezi  , related_name='typeMomayeziRelatedBehbod' ,on_delete=models.CASCADE)
    teamBehbod           = models.ForeignKey(MomayeziTeam , blank=True , null=True , related_name="teamBehbod" , on_delete = models.CASCADE )
    calenderBehbod= models.ForeignKey(CalenderMomayezi , blank=True , null=True , related_name="calenderBehbod" , on_delete = models.CASCADE )
    vahedBehbod= models.ForeignKey(Vahed , blank=True , null=True , related_name="vahedBehbod" , on_delete = models.CASCADE )
    systemBehbod= models.ForeignKey(Standard , blank=True , null=True , related_name="systemBehbod" , on_delete = models.CASCADE )
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title 
 


class AdamEntebagh(models.Model):
    typeMomayeziRelated = models.ForeignKey(TypeMomayezi  , related_name='typeMomayeziRelatedAdam' ,on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    
    teamAdamEntebagh           = models.ForeignKey(MomayeziTeam , blank=True , null=True , related_name="teamAdamEntebagh" , on_delete = models.CASCADE )
    calenderAdamEntebagh= models.ForeignKey(CalenderMomayezi , blank=True , null=True , related_name="calenderAdamEntebagh" , on_delete = models.CASCADE )
    vahedAdamEntebagh= models.ForeignKey(Vahed , blank=True , null=True , related_name="vahedAdamEntebagh" , on_delete = models.CASCADE )
    systemAdamEntebagh= models.ForeignKey(Standard , blank=True , null=True , related_name="systemAdamEntebagh" , on_delete = models.CASCADE )
    bandMomayeziAdamEntebagh   = models.ManyToManyField(RequirementStandards ,related_name="bandMomayeziAdamEntebagh" )
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title 
    
 


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'momayezi_team_request/{0}_{1}_{2}/{3}'.format(instance.memberMomayezi.user.id, instance.memberMomayezi.lastName , instance.memberMomayezi.firstName,filename)
class MomayeziTeamRequest(models.Model):
    
    REQUEST_STATUS  = (('accept','accept'),('reject','reject') ,('not','not')  )
    
    
    memberMomayezi   = models.ForeignKey(Profile , related_name="memberMomayeziRequest",blank=True , null=True , on_delete=models.CASCADE)
    sabegheYear      = models.IntegerField(null=True, blank=True  )
    document         = models.FileField(upload_to=(user_directory_path) ,blank=True, null=True)
    status           = models.CharField(max_length=75, choices= REQUEST_STATUS ,default='not' )
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "درخواست عضویت در تیم ممیزی"
        verbose_name_plural = "درخواست عضویت در تیم ممیزی"
    
    def __str__(self):
        return  str(self.memberMomayezi)


  

class MomayeziActivityManager(models.Model):
    ACTIVITY_STATUS  = (('done','انجام شده'),('doing','درحال انجام') , ('doNot' , 'انجام نشد'))
    ACTIVITY_LIST    = (('team','تعریف تیم'),('calender','برنامه زمانی'),('cheakListQuestion','چک لیست سوال'),('cheakList','چک لیست') , ('report' , 'گزارش') , ('finish' , 'پایان'))
    sender           = models.ForeignKey(Profile, null=True,  blank=True , related_name='SenderProfileMomayezi' , on_delete = models.CASCADE)
    reciver          = models.ForeignKey(Profile, null=True,  blank=True , related_name='ReciverProfileMomayezi' , on_delete = models.CASCADE)
    status           = models.CharField(max_length=75, choices= ACTIVITY_STATUS ,default='doing' )
    activity         = models.CharField(max_length=75, choices= ACTIVITY_LIST  )
    calender         = models.ForeignKey(CalenderMomayezi , null=True , blank=True , related_name='calenderMomayeziActivity' , on_delete = models.CASCADE )
    typeMomayeziRelated = models.ForeignKey(TypeMomayezi , default=1, related_name='typeMomeyeziRelatedActivity' , on_delete = models.CASCADE)
    
    previousActivity = models.ForeignKey('self' , null=True,  blank=True , related_name='PrActivityMomayezi' , on_delete = models.CASCADE)
    nextActivity     = models.ForeignKey('self' , null=True,  blank=True , related_name='NeActivityMomayezi' , on_delete = models.CASCADE)
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "مدیریت فعالیت های ممیزی   "
        verbose_name_plural = "مدیریت فعالیت های ممیزی   "
    
    def __str__(self):
        return str(self.id)  + " " + str(self.sender)
    
    
  
  
class RoleMomayezi(models.Model):
    title = models.CharField(max_length=100)
    

    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "نقش های ممیزی"
        verbose_name_plural = "نقش های ممیزی"
    
    def __str__(self):
        return self.title 

class QuestionMomayeziList(models.Model):

    vahedQuestion        = models.ForeignKey(Vahed , blank=True, null=True, related_name="vahedQuestion" , on_delete = models.CASCADE )
    question             = models.CharField(max_length=250,   )
    description          = models.TextField(null=True, blank=True ) 
    standardQuestion     = models.ForeignKey(Standard , blank=True, null=True, related_name="standardQuestion" , on_delete = models.CASCADE )
    requirementStandardQuestion  = models.ManyToManyField(RequirementStandards ,related_name="requirementStandardQuestion" )
    
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "سوالات ممیزی  "
        verbose_name_plural = "سوالات ممیزی  "
    
    def __str__(self):
        return self.vahedQuestion.title  
    

        
    
def user_directory_path_checklist(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'momayezi_checklist_document/{0}_{1}_{2}/{3}'.format(instance.activity.reciver.user.id, instance.activity.reciver.lastName , instance.activity.reciver.firstName,filename)
class CheckListMomayezi(models.Model):
    RESULT_STATUS  = (('ok','ok'),('Obs','Obs') ,('min','min')  , ('maj','maj')  )
    title                = models.TextField(null=True, blank=True )
    activity             = models.ForeignKey(MomayeziActivityManager,null=True, blank=True , related_name="activityCheckListMomayezi", on_delete=models.CASCADE)
    observed             = models.TextField(null=True, blank=True ) 
    result               = models.CharField(max_length=75, choices= RESULT_STATUS ,null=True, blank=True ) 
    question             = models.ForeignKey(QuestionMomayeziList , related_name="questionCheckListMomayezi", on_delete=models.CASCADE  , blank=True , null=True)
    typeMomayeziRelated  = models.ForeignKey(TypeMomayezi , default=1 , related_name="typeMomayeziRelatedCheckList", on_delete=models.CASCADE  )
    document             = models.FileField(upload_to=(user_directory_path_checklist) ,blank=True, null=True)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "چک لیست ممیزی"
        verbose_name_plural = "چک لیست ممیزی"
    
    def __str__(self):
        return self.title 
    

class ReportMomayezi(models.Model):
    RESULT_LIST    = (('ghovat','نقطه قوت') ,('behbod','فرصت بهبود'),('adam','عدم انطباق'),)

    report  = models.CharField(max_length=250)
    vahedRelated           = models.ForeignKey(Vahed , blank=True, null=True, related_name="vahedRelatedReport" , on_delete = models.CASCADE )
    typeMomayeziRelated    = models.ForeignKey(TypeMomayezi , blank=True, null=True, related_name="typeMomayeziRelatedReport" , on_delete = models.CASCADE )
    result           = models.CharField(max_length=75, choices= RESULT_LIST ,default='ghovat' )
    
    
    
    activityRelated    = models.ForeignKey(MomayeziActivityManager , blank=True, null=True, related_name="activityRelatedReport" , on_delete = models.CASCADE)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)
    
        



    def __str__(self):
        return self.report 



    
     
    
   