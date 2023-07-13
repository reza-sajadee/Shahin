from django.db import models

# Create your models here.


class External(models.Model):
    organization            = models.CharField(max_length=250)
    title                   = models.CharField(max_length=250)
    time                    = models.CharField(max_length=250)
    how                     = models.CharField(max_length=250)
    actor                   = models.CharField(max_length=250)
    reciver                 = models.CharField(max_length=250)
    
    
    class Meta:
        verbose_name = "جدول ارتباطات خارحی "
        verbose_name_plural = "جدول ارتباطات خارحی "
    
