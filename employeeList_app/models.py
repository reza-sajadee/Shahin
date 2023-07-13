from django.db import models
from django.db.models.fields.related import ForeignKey
from import_export import resources
from import_export.admin import ImportExportModelAdmin

#جدول لیست پرسنلی
class EmployeeList(models.Model):
    firstName            = models.CharField(max_length=100)
    lastName             = models.CharField(max_length=100)
    idNumber             = models.CharField(max_length=100)
    employeeNumber       = models.CharField(max_length=100)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)
 

    def __str__(self):
        return self.employeeNumber 
    
    

class EmployeeSuperiorList(models.Model):
    employeeNumber       = models.ForeignKey('EmployeeList' , blank=True, null=True, related_name="EmployeeNo" , on_delete = models.CASCADE )
    superiorNumber       = models.ForeignKey('EmployeeList' , blank=True, null=True, related_name="superiorNo" , on_delete = models.CASCADE )

 

  