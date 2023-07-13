from django.contrib import admin
from .models import CorrectiveAction ,TextDataBase , BoolDataBase,CorrectiveActionActivityManager , ConfirmationDataBase
from import_export.admin import ImportExportModelAdmin
from .resources import CorrectiveActionResource ,TextDataBaseResource ,BoolDataBaseResource , CorrectiveActionActivityManagerResource ,ConfirmationDataBaseResource


@admin.register(CorrectiveAction)
class CorrectiveActionAdmin(ImportExportModelAdmin):
     list_display = ('demandantId','problem' )
     list_filter = ('demandantId','problem' )
     search_fields = ('demandantId','problem')
     resource_class  = CorrectiveActionResource
@admin.register(TextDataBase)
class TextDataBaseAdmin(ImportExportModelAdmin):
     list_display = ('title', )
     list_filter = ('title', )
     search_fields = ('title',)
     resource_class  = TextDataBaseResource
@admin.register(BoolDataBase)
class BoolDataBaseAdmin(ImportExportModelAdmin):
     list_display = ('title', )
     list_filter = ('title', )
     search_fields = ('title',)
     resource_class  = BoolDataBaseResource
@admin.register(ConfirmationDataBase)
class ConfirmationDataBaseAdmin(ImportExportModelAdmin):
     list_display = ('title', )
     list_filter = ('title', )
     search_fields = ('title',)
     resource_class  = ConfirmationDataBaseResource
@admin.register(CorrectiveActionActivityManager)
class CorrectiveActionActivityManagerAdmin(ImportExportModelAdmin):
     list_display = ('status' ,'activity' ,'CorrectiveActionRelated' )
     list_filter = ('status'  ,'activity' ,'CorrectiveActionRelated')
     search_fields = ('status' ,'activity' ,'CorrectiveActionRelated')
     resource_class  = CorrectiveActionActivityManagerResource



# Register your models here.
