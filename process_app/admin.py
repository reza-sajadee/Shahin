from django.contrib import admin
from .models import Nahiye , Hoze , Group  ,Process , ProcessDocument,ProcessDescription ,ProcessFrom ,ProcessTo
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .resources import NahiyeResource , HozeResource , GroupResource , ProcessResource  , ProcessDocumentResource, ProcessDescriptionResource ,ProcessFromResource ,ProcessToResource


# Register your models here.



@admin.register(Nahiye)
class NahiyeAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('title' , 'created_at' , 'updated_at')
    # فیلتر های نمایش داده شده         
     list_filter = ('title' , )
    # فیلد های قابل سرچ         
     search_fields = ('title' ,)
     resource_class  = NahiyeResource
     
 
     
@admin.register(Hoze)
class HozeAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('title' , 'created_at' , 'updated_at')
    # فیلتر های نمایش داده شده         
     list_filter = ('title' , )
    # فیلد های قابل سرچ         
     search_fields = ('title' ,)
     resource_class  = HozeResource
     
     
 
     
@admin.register(Group)
class GroupAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('title' , 'created_at' , 'updated_at')
    # فیلتر های نمایش داده شده         
     list_filter = ('title' , )
    # فیلد های قابل سرچ         
     search_fields = ('title' ,)
     resource_class  = GroupResource
     
     

@admin.register(Process)
class ProcessAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('title' , 'ownerVahed' )
    # فیلتر های نمایش داده شده         
     list_filter = ('title' , )
    # فیلد های قابل سرچ         
     search_fields = ('title' ,)
     resource_class  = ProcessResource
    
@admin.register(ProcessDocument)
class ProcessDocumentAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('process' , )
    # فیلتر های نمایش داده شده         
     list_filter = ('process' , )
    # فیلد های قابل سرچ         
     search_fields = ('process' ,)
     resource_class  = ProcessDocumentResource
     

@admin.register(ProcessDescription)
class ProcessDescriptionAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('ProcessDocumentRelated',  )
    # فیلتر های نمایش داده شده         
     list_filter = ('ProcessDocumentRelated' , )
    # فیلد های قابل سرچ         
     search_fields = ('ProcessDocumentRelated' ,)
     resource_class  = ProcessDescriptionResource


@admin.register(ProcessFrom)
class ProcessFromAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('id',  )
    # فیلتر های نمایش داده شده         
     list_filter = ('id' , )
    # فیلد های قابل سرچ         
     search_fields = ('id' ,)
     resource_class  = ProcessFromResource

@admin.register(ProcessTo)
class ProcessToAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('id',  )
    # فیلتر های نمایش داده شده         
     list_filter = ('id' , )
    # فیلد های قابل سرچ         
     search_fields = ('id' ,)
     resource_class  = ProcessToResource

