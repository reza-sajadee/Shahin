from django.db import models

# Create your models here.
class Faq(models.Model):
    TYPE_STATUS  = (('learn','آموزشی'), )
 
    question     = models.CharField(max_length=250, verbose_name='سوال', blank=True , null=True) 
    answer         = models.TextField(null=True, blank=True ) 
    typeQuestion = models.CharField(max_length=250 , blank=True , null=True ,choices=TYPE_STATUS , verbose_name='روند شاخص') 
    
    
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = " سوالات متداول  "
        verbose_name_plural = "سوالات متداول  "
    def __str__(self):
        return str(self.id )