from django.contrib import admin
from .models import Faq 
from import_export.admin import ImportExportModelAdmin 
from .resources import  FaqResource 


@admin.register(Faq)
class FaqAdmin(ImportExportModelAdmin):
     list_display = ('id' ,)
     list_filter = ('id' ,)
     search_fields = ('id' ,)
     resource_class  = FaqResource