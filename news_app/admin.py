from django.contrib import admin
from .resources import CategoriyResource ,NewsResource
from .models import Categoriy , News
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.
# Register your models here.
@admin.register(Categoriy)
class CategoriyAdmin(ImportExportModelAdmin):
     list_display = ('title' , )
     list_filter = ('title' , )
     search_fields = ('title' ,)
     resource_class  = CategoriyResource
     

@admin.register(News)
class NewsAdmin(ImportExportModelAdmin):
     list_display = ('id' , 'title' , 'NewsCategoriy' )
     list_filter = ('NewsCategoriy' , )
     search_fields = ('title' ,)
     resource_class  = NewsResource
     
