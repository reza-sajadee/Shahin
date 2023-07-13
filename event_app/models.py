from django.db import models
from datetime import datetime
from profile_app.models import Profile
# Create your models here.

class EventAbstract(models.Model):
    """ Event abstract model """

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self):
        events = Event.objects.filter( is_active=True, is_deleted=False)
        return events

    def get_running_events(self):
        running_events = Event.objects.filter(
            
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_events



class Event(EventAbstract):
    """ Event model """
    COLOR_STATUS  = (('#F44335 ','قرمز'),('#4CAF50','سبز') , ('#fb8c00','نارنجی') )
    DISPLAY_STATUS  = (('auto','خودکار'),('list-item','نقطه') , )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profileEvent")
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    start = models.DateField()
    end = models.DateField()
    color = models.CharField(max_length=8 ,  choices= COLOR_STATUS , blank=True , null=True)
    
    display = models.CharField(max_length=20 ,   choices= DISPLAY_STATUS ,default='auto' , blank=True , null=True)
    objects = EventManager()

    class Meta:
        verbose_name = " رویداد"
        verbose_name_plural = " رویداد"
    def __str__(self):
        return self.title

