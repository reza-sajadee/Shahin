from django.contrib import admin
from .models import  Notifications
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .resources import NotificationsResource 
# Register your models here.standardTableResource


# Register your models here.
@admin.register(Notifications)
class NotificationsAdmin(ImportExportModelAdmin):
     list_display = ('title','personalStatus' )
     list_filter = ('title','personalStatus' ,'recivers' )
     search_fields = ('title','personalStatus')
     resource_class  = NotificationsResource
     
     