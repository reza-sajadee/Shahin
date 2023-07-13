from django.contrib import admin
from .models import Profile
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .resources import ProfileResource 


# Register your models here.



@admin.register(Profile)
class NahiyeAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('user' , 'firstName' , 'lastName')
    # فیلتر های نمایش داده شده         
     list_filter = ('user' ,'lastName' , )
    # فیلد های قابل سرچ         
     search_fields = ('user' ,)
     resource_class  = ProfileResource
     
 