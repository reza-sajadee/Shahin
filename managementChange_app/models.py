from django.db import models
from profile_app.models import Profile
from standardTable_app.models import Standard
# Create your models here.
from jalali_date import date2jalali 
from organization_app.models import Vahed

class ProfileManagementChange(models.Model):
    
    VahedChange = models.ForeignKey(Vahed  , related_name="VahedChange" , on_delete=models.CASCADE)
    code = models.CharField(max_length=250 , blank=True , null=True)
    typeChange = models.CharField(max_length=250 , blank=True , null=True)
    subjectChange = models.CharField(max_length=250 , blank=True , null=True)
    locationChange = models.TextField( blank=True , null=True)
    discription = models.TextField( blank=True , null=True)
    resonChange = models.TextField( blank=True , null=True)
    goalChange = models.TextField( blank=True , null=True)
    effectChange = models.TextField( blank=True , null=True)
    effectChangeProfile = models.ForeignKey(Profile  , related_name="effectChangeProfile" , on_delete=models.CASCADE)
    changeProfile  = models.ForeignKey(Profile  , related_name="changeProfile" , on_delete=models.CASCADE)
    
    firstCheckChange = models.TextField( blank=True , null=True)
    firstCheckChangeProfile = models.ForeignKey(Profile  , related_name="firstCheckChangeProfile" , on_delete=models.CASCADE)
    preparationChange = models.TextField( blank=True , null=True)
    preparationChangeProfile = models.ForeignKey(Profile  , related_name="preparationChangeProfile" , on_delete=models.CASCADE)
    effectiveChange = models.TextField( blank=True , null=True)
    effectiveChangeProfile = models.ForeignKey(Profile  , related_name="effectiveChangeProfile" , on_delete=models.CASCADE)
    criterionChange = models.TextField( blank=True , null=True)
    criterionChangeProfile = models.ForeignKey(Profile  , related_name="criterionChangeProfile" , on_delete=models.CASCADE)
    resultChnage = models.TextField( blank=True , null=True)
    resultChnageProfile = models.ForeignKey(Profile  , related_name="resultChnageProfile" , on_delete=models.CASCADE)
    
    
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = " پروفایل بازنگری و مدیریت"
        verbose_name_plural = " پروفایل بازنگری و مدیریت"
        
    def __str__(self):
        return str(self.id)  
