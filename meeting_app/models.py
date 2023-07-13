from django.db import models
from profile_app.models import Profile
# Create your models here.
from organization_app.models import JobBank
from jalali_date import date2jalali 

class MeetingProfile(models.Model):
    MEETING_TYPE_STATUS  = (('meet','جلسه'),('committee','کمیته') , ('review','بازنگری') )
    meetingType    = models.CharField(max_length=100 , choices= MEETING_TYPE_STATUS ,default='meet' )
    title          = models.CharField(max_length=100 , blank=True , null=True)
    responsible    =  models.ForeignKey(JobBank , related_name='responsibleMetting' ,blank=True , null=True , on_delete = models.CASCADE , verbose_name='دبیر ')
    manager    =  models.ForeignKey(JobBank , related_name='manager' ,blank=True , null=True , on_delete = models.CASCADE , verbose_name='دبیر ')
    firstSuccessor    =  models.ForeignKey(JobBank , related_name='firstSuccessor' ,blank=True , null=True , on_delete = models.CASCADE , verbose_name='دبیر ')
    secondSuccessor    =  models.ForeignKey(JobBank , related_name='secondSuccessor' ,blank=True , null=True , on_delete = models.CASCADE , verbose_name='دبیر ')
    membersPrimary          = models.ManyToManyField(JobBank)
    text           = models.TextField(null=True, blank=True ) 
    
    created_at           = models.DateTimeField(auto_now_add=True , blank=True,null=True)
    updated_at           = models.DateTimeField(auto_now=True , blank=True,null=True)
    class Meta:
        verbose_name = "پروفایل جلسات"
        verbose_name_plural = "پروفایل جلسات"
    
    def __str__(self):
        return str(self.id)  + " " + str(self.title)


    
class Meeting(models.Model):
    meetingProfileRelated      = models.ForeignKey(MeetingProfile ,blank=True , null=True , related_name='MeetingProfileRelated'  , on_delete = models.CASCADE , verbose_name='پروفایل جلسه مرتبط  ')
    title = models.CharField(max_length=100 , blank=True , null=True)
    description  = models.TextField(null=True, blank=True ) 
    complate  = models.BooleanField(default=False)


    

    created_at           = models.DateTimeField(auto_now_add=True , blank=True,null=True)
    updated_at           = models.DateTimeField(auto_now=True , blank=True,null=True)
    class Meta:
        verbose_name = " جلسه"
        verbose_name_plural = " جلسه"
    
    def __str__(self):
        return str(self.title)  


class Member(models.Model):
    JobBankRelated       = models.ForeignKey(JobBank,blank=True, null=True, related_name='JobBankRelated' , on_delete=models.CASCADE)
    meetingRelated       = models.ForeignKey(Meeting ,blank=True , null=True , related_name='MemberRelated'  , on_delete = models.CASCADE , verbose_name='پروفایل جلسه مرتبط ')
    present              = models.BooleanField(default=True)
    created_at           = models.DateTimeField(auto_now_add=True , blank=True,null=True)
    updated_at           = models.DateTimeField(auto_now=True , blank=True,null=True)
    class Meta:
        verbose_name = "حاظرین جلسات"
        verbose_name_plural = "حاظرین جلسات"
    
    def __str__(self):
        return str(self.id) 

class MeetingDate(models.Model):
    meetingRelated = models.ForeignKey(Meeting ,blank=True , null=True , related_name='MeetingRelatedDate'  , on_delete = models.CASCADE , verbose_name='پروفایل جلسه مرتبط ')
    meetingDate = models.DateField()
    meetingTime = models.TimeField()
    meetingTimeDuration = models.TimeField()
    meetingPlace   = models.CharField(max_length=250 , blank=True , null=True)
    
   
    
    created_at           = models.DateTimeField(auto_now_add=True , blank=True,null=True)
    updated_at           = models.DateTimeField(auto_now=True , blank=True,null=True)
    class Meta:
        verbose_name = "تاریخ جلسات"
        verbose_name_plural = "تاریخ جلسات"
    
    def __str__(self):
        return str(self.meetingDate)  

def get_jalali_date(self):
        return date2jalali(self.meetingDate)
class MeetingInvitation(models.Model):
    meetingRelated = models.ForeignKey(Meeting ,blank=True , null=True , related_name='MeetingRelatedInvitation'  , on_delete = models.CASCADE , verbose_name='پروفایل جلسه مرتبط ')
    title = models.CharField(max_length=100 , blank=True , null=True)
    text  = models.TextField(null=True, blank=True ) 
    created_at           = models.DateTimeField(auto_now_add=True , blank=True,null=True)
    updated_at           = models.DateTimeField(auto_now=True , blank=True,null=True)
    class Meta:
        verbose_name = "دعوت نامه جلسه"
        verbose_name_plural = "دعوت نامه جلسه"
    
    def __str__(self):
        return str(self.meetingRelated.id)  
    
    
class MeetingMember(models.Model):
    meetingRelated      = models.ForeignKey(Meeting ,blank=True , null=True , related_name='MeetingRelatedMember'  , on_delete = models.CASCADE , verbose_name='تاریخ جلسه مرتبط ')
    
    membersSecondary        = models.ManyToManyField(Member , related_name='membersSecondary')
    membersOther            = models.TextField(null=True, blank=True ) 
    compated             = models.BooleanField(default=False)

    created_at           = models.DateTimeField(auto_now_add=True , blank=True,null=True)
    updated_at           = models.DateTimeField(auto_now=True , blank=True,null=True)
    class Meta:
        verbose_name = "اعضای جلسه"
        verbose_name_plural = "اعضای جلسه"
    
    def __str__(self):
        return str(self.meetingRelated.id)  



class MeetingAgenda(models.Model):
    meetingRelated = models.ForeignKey(Meeting ,blank=True , null=True , related_name='MeetingRelatedAgenda'  , on_delete = models.CASCADE , verbose_name='پروفایل جلسه مرتبط ')
    title = models.CharField(max_length=100 , blank=True , null=True)
    text  = models.TextField(null=True, blank=True ) 
    timeDuration = models.TimeField(blank=True , null=True)
    responsible    =  models.ForeignKey(JobBank , related_name='responsibleMettingAgenda' ,blank=True , null=True , on_delete = models.CASCADE , verbose_name='دبیر ')
    created_at           = models.DateTimeField(auto_now_add=True , blank=True,null=True)
    updated_at           = models.DateTimeField(auto_now=True , blank=True,null=True)
    class Meta:
        verbose_name = "دستور  جلسه"
        verbose_name_plural = "دستور  جلسه"
    
    def __str__(self):
        return str(self.meetingRelated.id)  

def user_directory_path_meetingDocument(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'meeting_document/{0}'.format( filename)
# class MeetingMinute(models.Model):
#     meetingRelated = models.ForeignKey(Meeting ,blank=True , null=True , related_name='MeetingRelatedMinute'  , on_delete = models.CASCADE , verbose_name='پروفایل جلسه مرتبط ')
#     presents =  models.ManyToManyField(JobBank , related_name='membersPresents')
#     absents =  models.ManyToManyField(JobBank , related_name='membersAbsents')
#     persentDocument          = models.FileField(upload_to=(user_directory_path_meetingDocument) ,blank=True, null=True)
#     minuteDocument          = models.FileField(upload_to=(user_directory_path_meetingDocument) ,blank=True, null=True)
    
    
    
#     created_at           = models.DateTimeField(auto_now_add=True , blank=True,null=True)
#     updated_at           = models.DateTimeField(auto_now=True , blank=True,null=True)
#     class Meta:
#         verbose_name = "صورت  جلسه"
#         verbose_name_plural = "صورت  جلسه"
    
#     def __str__(self):
#         return str(self.meetingRelated.id)  




class MeetingEnactment(models.Model):
    meetingRelated       = models.ForeignKey(Meeting ,blank=True , null=True , related_name='MeetingRelatedEnactment'  , on_delete = models.CASCADE , verbose_name='پروفایل جلسه مرتبط ')
    title                = models.CharField(max_length=100 , blank=True , null=True)
    responsibleExecutive =  models.ForeignKey(JobBank , blank=True , null=True , related_name='responsibleMeetingEnactmentExecutive'  , on_delete = models.CASCADE , verbose_name='مسئول اجرا مصوبه ')
    responsibleFollow    =  models.ForeignKey(JobBank , blank=True , null=True , related_name='responsibleMeetingEnactmentFollow'  , on_delete = models.CASCADE , verbose_name='مسئول پیگیری اجرا مصوبه ')
    deadLine             = models.DateTimeField( null=True, blank=True)
    
    
    created_at           = models.DateTimeField(auto_now_add=True , blank=True,null=True)
    updated_at           = models.DateTimeField(auto_now=True , blank=True,null=True)
    class Meta:
        verbose_name = "صورت  جلسه"
        verbose_name_plural = "صورت  جلسه"
    
    def __str__(self):
        return str(self.meetingRelated.id)  


def user_directory_path_meetingDocument(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'meeting_document/{0}'.format( filename)
class MeetingDocument(models.Model):
    meetingRelated = models.ForeignKey(Meeting ,blank=True , null=True , related_name='MeetingRelatedDocument'  , on_delete = models.CASCADE , verbose_name='پروفایل جلسه مرتبط ')
    
    persentDocument          = models.FileField(upload_to=(user_directory_path_meetingDocument) ,blank=True, null=True)
    minuteDocument          = models.FileField(upload_to=(user_directory_path_meetingDocument) ,blank=True, null=True)
    
    
    
    created_at           = models.DateTimeField(auto_now_add=True , blank=True,null=True)
    updated_at           = models.DateTimeField(auto_now=True , blank=True,null=True)
    class Meta:
        verbose_name = "فایل  جلسه"
        verbose_name_plural = "فایل  جلسه"
    
    def __str__(self):
        return str(self.meetingRelated.id)  

class MeetingPlan(models.Model):
    meetingRelated = models.ForeignKey(Meeting ,blank=True , null=True , related_name='MeetingRelatedPlan'  , on_delete = models.CASCADE , verbose_name='پروفایل جلسه مرتبط ')
    
    planDocument          = models.FileField(upload_to=(user_directory_path_meetingDocument) ,blank=True, null=True)
    
    
    
    
    created_at           = models.DateTimeField(auto_now_add=True , blank=True,null=True)
    updated_at           = models.DateTimeField(auto_now=True , blank=True,null=True)
    class Meta:
        verbose_name = "طرح  جلسه"
        verbose_name_plural = "طرح  جلسه"
    
    def __str__(self):
        return str(self.meetingRelated.id)  


 

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
    CONFIRM_STATUS  = (('yes','بله'),('no','خیر'),('pending','در دست بررسی') )
    title   = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile ,related_name='confirmationMeetingProfile' , on_delete = models.CASCADE  ) 
    confirm = models.CharField(max_length=75, choices= CONFIRM_STATUS , default='pending' )
    text  = models.TextField(null=True, blank=True ) 
    MeetingRelated = models.ForeignKey(Meeting ,related_name='MeetingRelatedConfirmation' , on_delete = models.CASCADE )
    class Meta:
        verbose_name = "دیتابیس  کانفرم شدن"
        verbose_name_plural = "دیتابیس  کانفرم شدن"
    
    def __str__(self):
        return str(self.id)  + " " + str(self.title) 


# def user_directory_path_correctiveAction(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#         return 'corrective_action_document/{0}_{1}_{2}/{3}'.format(instance.reciver.user.id, instance.reciver.lastName , instance.reciver.firstName,filename)
# class MeetingActivityManager(models.Model):
#     ACTIVITY_STATUS  = (('done','done'),('doing','doing'), ('completed' , 'completed') )
#     ACTIVITY_LIST    = (('description','شرح مسئله/ درخواست'),('barresiMafogh','بررسی درخواست توسط مافوق' ),('executiveUnit','تعیین واحد مجری ') , ('register' , 'ثبت اطلاعات پایه'),('barresiModir','بررسی درخواست توسط مدیر') ,('cause','علت و ریشه ') ,('barresiMoaven','بررسی درخواست توسط معاون') , ('definitionCorrectiveaAtion','تعریف اقدام اصلاحی') ,('ejraNatije','ثبت نتیجه اقدام') ,('confirmRiportMotevali' , 'تایید گزارش  توسط واحد متولی'),('confirmRiportModir' , 'تایید گزارش  توسط مدیر دفتر توسعه مدیریت و تحقیقات') , ('effective' , 'اثربخشی'))
#     sender           = models.ForeignKey(Profile, null=True,  blank=True , related_name='SenderProfileCorrective' , on_delete = models.CASCADE)
#     reciver          = models.ForeignKey(Profile, null=True,  blank=True , related_name='ReciverProfileCorrective' , on_delete = models.CASCADE)
#     status           = models.CharField(max_length=75, choices= ACTIVITY_STATUS ,default='doing' )
#     activity         = models.CharField(max_length=75, choices= ACTIVITY_LIST  )
#     MeetingRelated  = models.ForeignKey(Meeting , related_name='MeetingRelated' , on_delete = models.CASCADE, null=True,  blank=True )
#     texts            = models.ManyToManyField(TextDataBase ,related_name="textData"   )
#     bools            = models.ManyToManyField(BoolDataBase ,related_name="BoolData"  )
#     file             = models.FileField(upload_to=(user_directory_path_correctiveAction) ,blank=True, null=True)
#     startTiem        = models.DateTimeField( null=True, blank=True)
#     deadLine         = models.DateTimeField( null=True, blank=True)
#     previousActivity = models.ForeignKey('self' , null=True,  blank=True , related_name='PrActivityMeeting' , on_delete = models.CASCADE)
#     nextActivity     = models.ForeignKey('self' , null=True,  blank=True , related_name='NeActivityMeeting' , on_delete = models.CASCADE)
#     confirmations    = models.ForeignKey(ConfirmationDataBase ,related_name="confirmationData" , on_delete = models.CASCADE , null=True,  blank=True)
#     created_at       = models.DateTimeField(auto_now_add=True)
#     updated_at       = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         verbose_name = "مدیریت فعالیت های اقدام اصلاحی   "
#         verbose_name_plural = "مدیریت فعالیت های اقدام اصلاحی   "
    
#     def __str__(self):
#         return str(self.id)  + " " + str(self.sender)
    
#     def lastStep(self):
#         last = self
#         while(True):

#             if(last.nextActivity != None):
               
#                 last = last.nextActivity
#             else:
#                 return last
            
#     def firstStep(self):
#         first = self
#         while(True):

#             if(first.previousActivity != None):
            
#                 first = first.previousActivity
#             else:
#                 return first

#     def listActivity(self):
#         listItem = []
#         item = self
       
#         while(True):
           
#             if(item.previousActivity != None):
               
#                 listItem.append(item)
#                 item = item.previousActivity
#             else:
#                 listItem.append(item)
#                 break
#         New_list = listItem.copy()
#         New_list.reverse()
        
      
#         return New_list
            
#     def allActivityList(self):
#         selected = self.firstStep()
#         listActivity = []
#         listActivity.append(selected)

#         while(True):
#             if(selected.nextActivity !=None):
#                 listActivity.append(selected.nextActivity)
#                 selected = selected.nextActivity
#             else:
#                 break
#         return listActivity

#     def findStep(self , step):
#         item = self
#         while(True):
      
#             if(item.activity == step):
#                 break
#             else:
#                 if(item.previousActivity is not None):
#                     item = item.previousActivity
#                 else:
#                     item = None
#                     break
#         return (item)

        