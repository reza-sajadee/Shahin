from django.contrib import admin
from .models import ReportActivityManager , Report 
from import_export.admin import ImportExportModelAdmin
from .resources import  ReportActivityManagerResource  , ReportResource 


@admin.register(Report)
class ReportAdmin(ImportExportModelAdmin):
     list_display = ('id' ,)
     list_filter = ('id' ,)
     search_fields = ('id' ,)
     resource_class  = ReportResource
@admin.register(ReportActivityManager)
class ReportActivityManagerAdmin(ImportExportModelAdmin):
     list_display = ('id', )
     list_filter = ('id', )
     search_fields = ('id',)
     resource_class  = ReportActivityManagerResource
