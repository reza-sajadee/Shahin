from django.db import models
from django.db.models.fields.related import ForeignKey



class Dashboard(models.Model):
    name             = models.CharField(max_length=100)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
 

    def __str__(self):
        return self.name 