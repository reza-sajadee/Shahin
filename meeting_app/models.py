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
    MEMBER_TYPE  = (('pr','اعضای اصلی'),('sc','اعضای فرعی') , ('other','سایر') )
    JobBankRelated       = models.ForeignKey(JobBank,blank=True, null=True, related_name='JobBankRelated' , on_delete=models.CASCADE)
    meetingRelated       = models.ForeignKey(Meeting ,blank=True , null=True , related_name='MemberRelated'  , on_delete = models.CASCADE , verbose_name='پروفایل جلسه مرتبط ')
    otherPerson          = models.CharField(blank=True , null=True , max_length=150)
    present              = models.BooleanField(default=False)
    memberType           = models.CharField(max_length=100 , choices= MEMBER_TYPE ,default='pr' )
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
        verbose_name = "دعوت به جلسه جلسه"
        verbose_name_plural = "دعوت به جلسه جلسه"
    
    def __str__(self):
        return str(self.meetingRelated.id)  
    
    
class MeetingMember(models.Model):
    meetingRelated      = models.ForeignKey(Meeting ,blank=True , null=True , related_name='MeetingRelatedMember'  , on_delete = models.CASCADE , verbose_name='تاریخ جلسه مرتبط ')
    
    membersSecondary        = models.ManyToManyField(Member , related_name='membersSecondary')
    membersOther            = models.TextField(null=True, blank=True ) 
    complated             = models.BooleanField(default=False)

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
        verbose_name = "فایل ارائه  جلسه"
        verbose_name_plural = "فایل ارائه  جلسه"
    
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
