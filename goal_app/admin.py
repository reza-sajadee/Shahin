from django.contrib import admin
from .models import Objective 
from import_export.admin import ImportExportModelAdmin 
from .resources import  ObjectiveResource 


@admin.register(Objective)
class ObjectiveAdmin(ImportExportModelAdmin):
     list_display = ('id' ,)
     list_filter = ('id' ,)
     search_fields = ('id' ,)
     resource_class  = ObjectiveResource
