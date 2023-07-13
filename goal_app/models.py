from django.db import models
from organization_app.models import JobBank
# Create your models here.
class Objective(models.Model):
    TREND_STATUS  = (('upTrend','روند افزایشی'),('downTrend','روند کاهشی'),('side','روند ثابت') )
    principle = models.CharField(max_length=250, verbose_name='اصل', blank=True , null=True) 
    presppective = models.CharField(max_length=250, verbose_name='منظر', blank=True , null=True) 
    goal = models.CharField(max_length=250, verbose_name='هدف کلان', blank=True , null=True) 
    title = models.CharField(max_length=250, verbose_name='عنوان', blank=True , null=True) 
    index = models.CharField(max_length=250, verbose_name='شاخص', blank=True , null=True)
    trendIndex = models.CharField(max_length=250 , blank=True , null=True ,choices=TREND_STATUS , verbose_name='روند شاخص') 
    target = models.CharField(max_length=250, verbose_name='معیار', blank=True , null=True) 
    currentSituation = models.CharField(max_length=250, verbose_name='وضعیت موجود', blank=True , null=True) 
    owner = models.ForeignKey(JobBank , blank=True, null=True, related_name="ownerObjective" , on_delete = models.CASCADE )
    startLine             = models.DateTimeField( null=True, blank=True) 
    deadLine             = models.DateTimeField( null=True, blank=True)
    description  = models.TextField( blank=True, null=True,)
    previousObjective = models.ForeignKey('self' , null=True,  blank=True , related_name='PrObjective' , on_delete = models.CASCADE)
    nextObjective     = models.ForeignKey('self' , null=True,  blank=True , related_name='NeObjective' , on_delete = models.CASCADE)
    
   
    
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = " هدف خرد "
        verbose_name_plural = "هدف خرد "
    def __str__(self):
        return str(self.id )