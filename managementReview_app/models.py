from django.db import models
from profile_app.models import Profile
from standardTable_app.models import Standard
# Create your models here.
from jalali_date import date2jalali 
from organization_app.models import Vahed

class ProfileManagementReview(models.Model):
    
    systemProfileManagementReview = models.ForeignKey(Standard ,default=1  , related_name="systemProfileManagementReview" , on_delete=models.CASCADE)
    title                         = models.CharField(max_length=250 , blank=True , null=True)
    within                        = models.CharField(max_length=250 , blank=True , null=True)
    dabir                         =models.ForeignKey(Profile , related_name="dabirManagementReview" , on_delete=models.CASCADE , blank=True, null=True)
    members                       = models.ManyToManyField(Profile , related_name="membersManagementReview")              
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = " پروفایل بازنگری و مدیریت"
        verbose_name_plural = " پروفایل بازنگری و مدیریت"
        
    def __str__(self):
        return str(self.id)  
class InputManagementReview(models.Model):
    
    systemInputManagementReview = models.ForeignKey(Standard ,default=1  , related_name="systemInputManagementReview" , on_delete=models.CASCADE)
    title                  = models.CharField(max_length=250 , blank=True , null=True)


    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "ورودی های بازنگری و مدیریت"
        verbose_name_plural = "ورودی های بازنگری و مدیریت"
        
    def __str__(self):
        return str(self.id)  
   
class InviteManagementReview(models.Model):
    dateManagementReview   = models.DateTimeField( null=True, blank=True)
    locationManagementReview = models.TextField(max_length=250 , null=True , blank=True)
    ProfileManagementReviewRelated =models.ForeignKey(ProfileManagementReview , related_name="ProfileManagementReviewRelated" , on_delete=models.CASCADE , blank=True, null=True)
    guests                 = models.ManyToManyField(Profile , related_name="guestsManagementReview") 
    
    
    
    

    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = " دعوت نامه جلسه بازنگری مدیریت"
        verbose_name_plural = "دعوت نامه جلسه بازنگری مدیریت "
        
    def __str__(self):
        return str(self.id)  
    def get_jalali_date(self):
        return date2jalali(self.dateManagementReview)
    
class approveManagementReview(models.Model):
    
    ProfileManagementReviewApprovedRelated =models.ForeignKey(ProfileManagementReview , related_name="ProfileManagementReviewApprovedRelated" , on_delete=models.CASCADE , blank=True, null=True)
    title = models.TextField(max_length=250 , null=True , blank=True)
    executVahed = models.ManyToManyField(Vahed ,related_name="executVahedApprove"  )
    trackVahed = models.ManyToManyField(Vahed ,related_name="trackVahed"  )
    deadLine   = models.DateTimeField( null=True, blank=True)
    
    
    

    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "مصوبات جلسات"
        verbose_name_plural = "مصوبات جلسات"
        
    def __str__(self):
        return str(self.id)  
    def get_jalali_date(self):
        return date2jalali(self.deadLine)
    
