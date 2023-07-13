from django.db import models
from organization_app.models import JobBank
from profile_app.models import Profile
# Create your models here.
def user_directory_path_reoprt(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'report_document/{0}'.format( filename )    
class Report(models.Model):
    
    title                = models.CharField(max_length=100 , blank=True , null=True)
    description          = models.TextField(null=True, blank=True ) 
    document             = models.FileField(upload_to=(user_directory_path_reoprt) ,blank=True, null=True)
    referabl             = models.BooleanField(default=True) 
    forward             = models.BooleanField(default=True) 
    arcane               = models.BooleanField(default=False) 
                  
    

    

    created_at           = models.DateTimeField(auto_now_add=True , blank=True,null=True)
    updated_at           = models.DateTimeField(auto_now=True , blank=True,null=True)
    class Meta:
        verbose_name = " گزارش"
        verbose_name_plural = " گزارش"
    
    def __str__(self):
        return str(self.title)  
    

class ReportActivityManager(models.Model):
    ACTIVITY_STATUS  = (('done','done'),('doing','doing'), ('completed' , 'completed') )

    sender           = models.ForeignKey(Profile, null=True,  blank=True , related_name='SenderReport' , on_delete = models.CASCADE)
    reciver          = models.ForeignKey(Profile, null=True,  blank=True , related_name='ReciverReport' , on_delete = models.CASCADE)
    status           = models.CharField(max_length=75, choices= ACTIVITY_STATUS ,default='doing' )

    ReportRelated  = models.ForeignKey(Report , related_name='ReportRelated' , on_delete = models.CASCADE, null=True,  blank=True )
    text            = models.TextField(null=True, blank=True ) 
    document             = models.FileField(upload_to=(user_directory_path_reoprt) ,blank=True, null=True)
    
    startTime        = models.DateTimeField( null=True, blank=True)
    deadLine         = models.DateTimeField( null=True, blank=True)
    previousActivity = models.ForeignKey('self' , null=True,  blank=True , related_name='PrActivityReport' , on_delete = models.CASCADE)
    nextActivity     = models.ForeignKey('self' , null=True,  blank=True , related_name='NeActivityReport' , on_delete = models.CASCADE)
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "مدیریت فعالیت های  گزارش   "
        verbose_name_plural = "مدیریت فعالیت های گزارش    "
    
    def __str__(self):
        return str(self.id)  + " " + str(self.sender)
    
    def lastStep(self):
        last = self
        while(True):

            if(last.nextActivity != None):
               
                last = last.nextActivity
            else:
                return last
            
    def firstStep(self):
        first = self
        while(True):

            if(first.previousActivity != None):
            
                first = first.previousActivity
            else:
                return first

    def listActivity(self):
        listItem = []
        item = self
       
        while(True):
           
            if(item.previousActivity != None):
               
                listItem.append(item)
                item = item.previousActivity
            else:
                listItem.append(item)
                break
        New_list = listItem.copy()
        New_list.reverse()
        
      
        return New_list
            
    def allActivityList(self):
        selected = self.firstStep()
        listActivity = []
        listActivity.append(selected)

        while(True):
            if(selected.nextActivity !=None):
                listActivity.append(selected.nextActivity)
                selected = selected.nextActivity
            else:
                break
        return listActivity

    def findStep(self , step):
        item = self
        while(True):
      
            if(item.activity == step):
                break
            else:
                if(item.previousActivity is not None):
                    item = item.previousActivity
                else:
                    item = None
                    break
        return (item)
