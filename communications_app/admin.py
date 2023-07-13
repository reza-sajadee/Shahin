from django.contrib import admin
from .models import  External
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .resources import ExternalResource
# Register your models here.standardTableResource


# # Register your models here.
@admin.register(External)
class ExternalAdmin(ImportExportModelAdmin):
     list_display = ('id' , )
     list_filter = ('id' , )
     search_fields = ('id' ,)
     resource_class  = ExternalResource
     
     