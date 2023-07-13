from django.contrib import admin
from .models import ProfileManagementChange 
from import_export.admin import ImportExportModelAdmin
from .resources import ProfileManagementChangeResource 


@admin.register(ProfileManagementChange)
class ProfileManagementChangeAdmin(ImportExportModelAdmin):
     list_display = ('id', )
     list_filter = ('id', )
     search_fields = ('id',)
     resource_class  = ProfileManagementChangeResource
