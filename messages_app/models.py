from django.db import models
from organization_app.models import Hoze
from profile_app.models import Profile
# Create your models here.
from django.db.models.fields.related import ForeignKey , ManyToManyField
status_choices = (
    ("warning", "warning"),
    ("primary", "primary"),
    ("success", "success"),
    
)
personalStatus_choices = (
    ("read", "خوانده شده"),
    ("pending", "مشاهده نشده"),

    
)
icon_choices = (
    ("warning-sign2", "warning-sign"),
    ("check-all2", "check-all"),
    ("alarm2", "alarm"),
    
)

def user_directory_path_messageAttached(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        #return 'message_attached/{0}_{1}_{2}/{3}'.format(instance.reciver.user.id, instance.reciver.lastName , instance.reciver.firstName,filename)
        return 'message_attached'
class FileAttached(models.Model):
    
    fileAttached             = models.FileField(upload_to=(user_directory_path_messageAttached) ,blank=True, null=True)
    class Meta:
        verbose_name = "فایل "
        verbose_name_plural = "فایل "
    
    def __str__(self):
        return str(self.id)
class Messages(models.Model):
    
    title            = models.CharField(max_length=200)
    description      = models.TextField(blank = True)
    status           = models.CharField(max_length=100, choices=status_choices , default='success')
    personalStatus   = models.CharField(max_length=100, choices=personalStatus_choices , default='pending')
    icon             = models.CharField(max_length=100, choices=icon_choices ,  default='check-all2')
    reciver         = models.ForeignKey(Profile , related_name='reciverProfileMessage' , blank=True ,null=True , on_delete = models.CASCADE)
    sender           = models.ForeignKey(Profile , related_name='senderProfileMessage' , blank=True ,null=True , on_delete = models.CASCADE)
    link             = models.CharField(max_length=200 , default = '')
    files            = models.ManyToManyField(FileAttached)
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "پیغام "
        verbose_name_plural = "پیغام "
    
    def __str__(self):
        return self.title 


