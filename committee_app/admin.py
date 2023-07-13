from django.contrib import admin
from .models import  Committee
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .resources import CommitteeResource 
# Register your models here.standardTableResource


# Register your models here.
@admin.register(Committee)
class TypeMadrakAdmin(ImportExportModelAdmin):
     list_display = ('topic','title' )
     list_filter = ('topic','title' )
     search_fields = ('topic','title')
     resource_class  = CommitteeResource
     
     