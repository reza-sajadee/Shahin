from django.contrib import admin
from .models import PositionLevelList
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from positionLevelList_app.resources import PositionLevelListResource
# Register your models here.

#ادمین بخش ناحیه های فرآیندی


@admin.register(PositionLevelList)
class PositionLevelListAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('positionLevelCode','title' ,'created_at' , 'updated_at')
    # فیلتر های نمایش داده شده         
     list_filter = ('positionLevelCode','title')
    # فیلد های قابل سرچ         
     search_fields = ('positionLevelCode','title')
     resource_class  = PositionLevelListResource
     
