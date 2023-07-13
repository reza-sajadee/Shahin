from django.db import models
from django.db.models.fields.related import ForeignKey

#لیست سطح های سازمانی


class PositionLevelList(models.Model):
    title                = models.CharField(max_length=150)
    positionLevelCode      = models.CharField(max_length=15)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    
