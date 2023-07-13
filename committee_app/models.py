from django.db import models
from organization_app.models import Hoze
from profile_app.models import Profile
from organization_app.models import JobBank
# Create your models here.
from django.db.models.fields.related import ForeignKey , ManyToManyField
topic_choices = (
    ("شورا", "شورا "),
    ("کمیسیون", "کمیسیون"),
    ("کمیته", "کمیته"),
    ("کارگروه", "کارگروه"),
    ("هیأت", "هیأت"),
    ("جلسه", "جلسه"),
    ("سایر", "سایر"),
)
type_choices = (
    ("تصمیم مدیریتی", "تصمیم مدیریتی "),
    ("قانون", "قانون"),
    ("دستورالعمل", "دستورالعمل"),
    ("سیستم و استاندارد سازی", "سیستم و استاندارد سازی"),
    ("سایر", "سایر"),
)
class Committee(models.Model):
    
    topic            = models.CharField(max_length=100, choices=topic_choices)
    title            = models.CharField(max_length=200)
    mostanadGhanoni  = models.CharField(max_length=250)
    
    hoze             = models.ForeignKey(Hoze  , blank=True, null=True ,related_name="hozeOfCommittee" , on_delete=models.CASCADE)
    typeComittee     = models.CharField(max_length=100, choices=type_choices)
    members          = models.ManyToManyField(JobBank  , related_name="members")
    head             = models.ForeignKey(JobBank , related_name="headOfCommittee" , blank=True, null=True , on_delete=models.CASCADE)
    janeshinAval     = models.ForeignKey(JobBank , related_name="janeshinAval" , blank=True, null=True , on_delete=models.CASCADE)
    janeshinDovom    = models.ForeignKey(JobBank , related_name="janeshinDovom" , blank=True, null=True , on_delete=models.CASCADE)
    dabir            = models.ForeignKey(JobBank , related_name="dabir" , blank=True, null=True , on_delete=models.CASCADE)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "کمیته "
        verbose_name_plural = "کمیته "
    
    def __str__(self):
        return self.title 

