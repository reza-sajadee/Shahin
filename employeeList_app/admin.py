from django.contrib import admin
from .models import EmployeeList 
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .resources import EmployeeListResource
# Register your models here.

#ادمین بخش  لیست کارمندان


@admin.register(EmployeeList)
class EmployeeListAdmin(ImportExportModelAdmin):
     # آیتم های نمایش داده شده
     list_display = ('idNumber','firstName','lastName','employeeNumber','created_at' ,'updated_at')
     # فیلتر های نمایش داده شده 
     list_filter = ('idNumber','firstName','lastName','employeeNumber')
     # فیلد های قابل سرچ   
     search_fields = ('idNumber','firstName','lastName','employeeNumber')
     resource_class  = EmployeeListResource
