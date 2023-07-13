from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resources import fileProfileResource

# Register your models here.
from .models import fileProfile
@admin.register(fileProfile)
class fileProfileAdmin(ImportExportModelAdmin):
     list_display = ('id', )
     list_filter = ('id', )
     search_fields = ('id',)
     resource_class  = fileProfileResource