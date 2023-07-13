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

class Notifications(models.Model):
    
    title            = models.CharField(max_length=200)
    description      = models.TextField(blank = True)
    status           = models.CharField(max_length=100, choices=status_choices)
    personalStatus   = models.CharField(max_length=100, choices=personalStatus_choices , default='pending')
    icon             = models.CharField(max_length=100, choices=icon_choices , blank = True , null = True ,default='alarm') 
    recivers         = models.ForeignKey(Profile, on_delete = models.CASCADE)
    sender           = models.ForeignKey(Profile , related_name='senderProfile' , blank=True ,null=True , on_delete = models.CASCADE)
    link             = models.CharField(max_length=200 , default = '')
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "اطلاعیه "
        verbose_name_plural = "اطلاعیه "
    
    def __str__(self):
        return self.title 

