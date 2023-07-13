from django.contrib import admin
from .models import Rade,Hoze,Bakhsh,Daste,SatheVahed,TypePostSazmani,Vahed , SathPost ,IndexMahaleKhedmat , JobBank ,Post , PostDescription
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .resources import RadeResource , HozeResource , BakhshResource , DasteResource , SatheVahedResource , TypePostSazmaniResource , VahedResource ,VahedResource , SathPostResource ,IndexMahaleKhedmatResource , JobBankResource , PostResource   , PostDescriptionResource
# Register your models here.

#ادمین بخش سازمانی


@admin.register(Rade)
class RadeAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('title' , 'created_at' , 'updated_at')
    # فیلتر های نمایش داده شده         
     list_filter = ('title' , )
    # فیلد های قابل سرچ         
     search_fields = ('title' ,)
     resource_class  = RadeResource
     
     
@admin.register(Hoze)
class HozeAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('title' , 'created_at' , 'updated_at')
    # فیلتر های نمایش داده شده         
     list_filter = ('title' , )
    # فیلد های قابل سرچ         
     search_fields = ('title' ,)
     resource_class  = HozeResource
     
     
@admin.register(Bakhsh)
class BakhshAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('title' , 'created_at' , 'updated_at')
    # فیلتر های نمایش داده شده         
     list_filter = ('title' , )
    # فیلد های قابل سرچ         
     search_fields = ('title' ,)
     resource_class  = BakhshResource
     
     
@admin.register(Daste)
class DasteAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('title' , 'created_at' , 'updated_at')
    # فیلتر های نمایش داده شده         
     list_filter = ('title' , )
    # فیلد های قابل سرچ         
     search_fields = ('title' ,)
     resource_class  = DasteResource
     
     
@admin.register(SatheVahed)
class SatheVahedAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('title' , 'created_at' , 'updated_at')
    # فیلتر های نمایش داده شده         
     list_filter = ('title' , )
    # فیلد های قابل سرچ         
     search_fields = ('title' ,)
     resource_class  = SatheVahedResource
     
     
     
@admin.register(TypePostSazmani)
class TypePostSazmaniAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('title' , 'created_at' , 'updated_at')
    # فیلتر های نمایش داده شده         
     list_filter = ('title' , )
    # فیلد های قابل سرچ         
     search_fields = ('title' ,)
     resource_class  = TypePostSazmaniResource
     
     
     
@admin.register(Vahed)
class VahedAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('title' , 'created_at' , 'updated_at')
    # فیلتر های نمایش داده شده         
     list_filter = ('title' , )
    # فیلد های قابل سرچ         
     search_fields = ('title' ,)
     resource_class  = VahedResource

     

@admin.register(SathPost)
class SathPostAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('title' , 'created_at' , 'updated_at')
    # فیلتر های نمایش داده شده         
     list_filter = ('title' , )
    # فیلد های قابل سرچ         
     search_fields = ('title' ,)
     resource_class  = SathPostResource

     
@admin.register(IndexMahaleKhedmat)
class IndexMahaleKhedmatAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('title' ,'indexCode' , 'created_at' , 'updated_at')
    # فیلتر های نمایش داده شده         
     list_filter = ('title' , 'indexCode' )
    # فیلد های قابل سرچ         
     search_fields = ('title' , 'indexCode')
     resource_class  = IndexMahaleKhedmatResource
     
@admin.register(JobBank)
class JobBankAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('profile' , 'counter'   )
    # فیلتر های نمایش داده شده         
     list_filter = ('profile' , 'counter',   )
    # فیلد های قابل سرچ         
     search_fields = ('profile' , 'counter'  )
     resource_class  = JobBankResource
         


     
@admin.register(Post)
class PostAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('title' , 'vahed','SathPost','zarfiyateMojaz','janamayiFeli','indexMahaleKhedmat','RadePostSazmani','postMafogh' )
    # فیلتر های نمایش داده شده         
     list_filter = ('title' , 'vahed','SathPost','zarfiyateMojaz','janamayiFeli','indexMahaleKhedmat','RadePostSazmani','postMafogh' )
    # فیلد های قابل سرچ         
     search_fields = ('title' , 'vahed','SathPost','zarfiyateMojaz','janamayiFeli','indexMahaleKhedmat','RadePostSazmani','postMafogh' )
     resource_class  = PostResource
         


@admin.register(PostDescription)
class PostDescriptionAdmin(ImportExportModelAdmin):
    # آیتم های نمایش داده شده    
     list_display = ('id' ,  )
    # فیلتر های نمایش داده شده         
     list_filter = ( 'id' ,   )
    # فیلد های قابل سرچ       
     search_fields = ( 'id' , )
     resource_class  = PostDescriptionResource
         