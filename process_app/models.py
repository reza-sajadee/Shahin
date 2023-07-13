from django.db import models
from django.db.models.fields.related import ForeignKey
from organization_app.models import Vahed
# Create your models here.



class Nahiye(models.Model):
    title                = models.CharField(max_length=150)
    nahiyeCode           = models.CharField(max_length=15)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    


class Hoze(models.Model):
    title                = models.CharField(max_length=150)
    hozeCode     = models.CharField(max_length=15)
    nahiyeCode      = models.ForeignKey(Nahiye , blank=True, null=True, related_name="nahiye" , on_delete = models.CASCADE )
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    




class Group(models.Model):
    title                = models.CharField(max_length=150)
    groupCode            = models.CharField(max_length=15)
    hozeCode             = models.ForeignKey(Hoze , blank=True, null=True, related_name="hoze" , on_delete = models.CASCADE )
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    

class Process(models.Model):
    title                = models.CharField(max_length=150)
    processCode          = models.CharField(max_length=15)
    groupCode            = models.ForeignKey(Group , blank=True, null=True, related_name="group" , on_delete = models.CASCADE )
    ownerVahed           = models.ForeignKey(Vahed , blank=True, null=True, related_name="OwnerVahed", on_delete= models.CASCADE)
    impactFactor         = models.FloatField(null=True, blank=True)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    

class ProcessDocument(models.Model):
    process             = models.ForeignKey(Process , blank=True, null=True, related_name="process", on_delete= models.CASCADE)
    goalProcess         = models.TextField( blank=True , null=True)
    driverProcess       = models.TextField( blank=True , null=True)
    scopeProcess        =models.CharField(max_length=250 , blank=True , null=True)
    guidelinesProcess   =models.CharField(max_length=250 , blank=True , null=True)

    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = " شناسنامه فرآیند"
        verbose_name_plural = " شناسنامه فرآیند"
    def __str__(self):
        return self.process.title 
class ProcessFrom(models.Model):
    ProcessDocumentRealated             = models.ForeignKey(ProcessDocument, related_name="ProcessDocumentRealatedFrom", on_delete= models.CASCADE)
    inputProcess            = models.TextField(blank=True, null=True,)
    fromProcessRelated             = models.ForeignKey(Process , blank=True, null=True, related_name="fromProcessRelated", on_delete= models.CASCADE)
    fromBeneficiary = models.CharField(max_length=250 , blank=True , null=True)
    
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = " از فرآیند"
        verbose_name_plural = " از فرآیند"
    def __str__(self):
        return str(self.id)
class ProcessTo(models.Model):
    ProcessDocumentRealated             = models.ForeignKey(ProcessDocument , related_name="ProcessDocumentRealatedTo", on_delete= models.CASCADE)
    outputProcess            = models.TextField(blank=True, null=True,)
    toProcessRelated             = models.ForeignKey(Process , blank=True, null=True, related_name="toProcessRelated", on_delete= models.CASCADE)
    toBeneficiary = models.CharField(max_length=250 , blank=True , null=True)
    
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = " به فرآیند"
        verbose_name_plural = " به فرآیند"
    def __str__(self):
        return str(self.id )
    
class ProcessDescription(models.Model): 
    ProcessDocumentRelated = models.ForeignKey(ProcessDocument , blank=True, null=True, related_name="ProcessDocument", on_delete= models.CASCADE)
    activityDescription    = models.TextField(blank=True, null=True,)
    ownerActivity          = models.CharField(max_length=250 ,blank=True , null=True)
    activityDocumentation  = models.CharField(max_length=250 ,blank=True , null=True)

    description            = models.TextField( blank=True, null=True,)
    activityCondition      = models.TextField( blank=True, null=True,)

    created_at             = models.DateTimeField(auto_now_add=True)
    updated_at             = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = " شرح فرآیند"
        verbose_name_plural = " شرح فرآیند"    
    def __str__(self):
        return self.ProcessDocumentRelated.process.title
    
    
