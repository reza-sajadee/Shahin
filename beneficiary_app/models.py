from django.db import models

# Create your models here.


class BeneficiaryList(models.Model):
    
    
    
    tabaghe            = models.CharField(max_length=250)
    beneficiary        = models.CharField(max_length=250)
    manzar             = models.CharField(max_length=250)
    beneficiaryType    = models.CharField(max_length=250)
    beneficiaryHoze    = models.CharField(max_length=250)
    description        = models.CharField(max_length=250)
    address            = models.CharField(max_length=250)
    contact            = models.CharField(max_length=250)
    vaziyatNow         = models.CharField(max_length=250)
    vaiyatMatlob       = models.CharField(max_length=250)
    expectations       = models.CharField(max_length=250)
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "لیست ذینفعان سازمان"
        verbose_name_plural = "لیست ذینفعان سازمان"
    
    def __str__(self):
        
        return str(self.id)
    
    
    
class ClassificationBeneficiary(models.Model):
    
    title            = models.CharField(max_length=250)
    
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "طبقه بندی ذینفعان"
        verbose_name_plural = "طبقه بندی ذینفعان"
    
    def __str__(self):
        
        return str(self.id)
    
class GroupBeneficiary(models.Model):
    
    title            = models.CharField(max_length=250)
    classificationRelated            = models.ForeignKey( ClassificationBeneficiary, related_name='classificationRelatedGroup' , on_delete = models.CASCADE)
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "گروه ذینفعان"
        verbose_name_plural = "گروه ذینفعان"
    
    def __str__(self):
        
        return str(self.id)
class Beneficiary(models.Model):
    
    title            = models.CharField(max_length=250)
    groupRelated            = models.ForeignKey( GroupBeneficiary, related_name='groupRelatedBeneficiary' , on_delete = models.CASCADE)
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "ذینفعان"
        verbose_name_plural = "ذینفعان"
    
    def __str__(self):
        
        return str(self.id)
class CurrentNeed(models.Model):
    
    title            = models.CharField(max_length=250)
    beneficiaryRelated            = models.ForeignKey( Beneficiary, related_name='beneficiaryRelatedCurrent' , on_delete = models.CASCADE)
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "نیاز های فعلی"
        verbose_name_plural = "نیاز های فعلی"
    
    def __str__(self):
        
        return str(self.id)
class FutureExpectations(models.Model):
    
    title            = models.CharField(max_length=250)
    beneficiaryRelated            = models.ForeignKey( Beneficiary, related_name='beneficiaryRelatedFuture' , on_delete = models.CASCADE)
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "انتظارات آتی"
        verbose_name_plural = "انتظارات آتی"
    
    def __str__(self):
        
        return str(self.id)