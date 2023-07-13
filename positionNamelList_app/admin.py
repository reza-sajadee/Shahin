from django.contrib import admin
from .models import PositionNameList
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from positionNamelList_app.resources import PositionNameListResource
# Register your models here.

#ادمین بخش ناحیه های فرآیندی


@admin.register(PositionNameList)
class PositionNameListAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('positionNameCode','title' ,'created_at' , 'updated_at')
    # فیلتر های نمایش داده شده         
     list_filter = ('positionNameCode','title')
    # فیلد های قابل سرچ         
     search_fields = ('positionNameCode','title')
     esource_class  = PositionNameListResource
     
