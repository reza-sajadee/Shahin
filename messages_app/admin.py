from django.contrib import admin
from .models import  Messages , FileAttached
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .resources import    MessagesResource , FileAttachedResource
# Register your models here.standardTableResource


# Register your models here.
@admin.register(Messages)
class NotificationsAdmin(ImportExportModelAdmin):
     list_display = ('id',)
     list_filter = ('id',)
     search_fields = ('id',)
     resource_class  = MessagesResource
     
     
# Register your models here.
@admin.register(FileAttached)
class NotificationsAdmin(ImportExportModelAdmin):
     list_display = ('id',)
     list_filter = ('id',)
     search_fields = ('id',)
     resource_class  = FileAttachedResource
     
     