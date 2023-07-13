from django.contrib import admin
from .models import MostanadatDakheli , TypeMadrak , MostanadatKhareji ,TextDataBase ,BoolDataBase ,ConfirmationDataBase ,MostanadatDakheliChangeActivityManager ,MostanadatDakheliChange , RecordDataBase ,RecordChange , RecordChangeActivityManager
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .resources import MostanadatDakheliResource , TypeMadrakResource , MostanadatKharejiResource ,TextDataBaseResource ,BoolDataBaseResource ,ConfirmationDataBaseResource ,MostanadatDakheliChangeActivityManagerResource ,MostanadatDakheliChangeResource ,RecordDataBaseResource ,RecordChangeResource , RecordChangeActivityManagerResource
# Register your models here.standardTableResource





@admin.register(TypeMadrak)
class TypeMadrakAdmin(ImportExportModelAdmin):
     list_display = ('title','typeMadrakCode' )
     list_filter = ('title','typeMadrakCode' )
     search_fields = ('title','typeMadrakCode')
     resource_class  = TypeMadrakResource
     
     


@admin.register(MostanadatDakheli)
class MostanadatDakheliAdmin(ImportExportModelAdmin):
     list_display = ('title','dakheliSanadCode','tabaghbandi' ,'vahedMotevaliCode','vahedTaeidCode','vahedTasvibCode','vahedTaeidCode','typeMadrakCode','systemMortabetCode' , 'outdated'  )
     list_filter = ('tabaghbandi' ,'typeMadrakCode','systemMortabetCode' , 'outdated','updated_at' )
     search_fields = ('title','dakheliSanadCode','tabaghbandi' ,'vahedMotevaliCode','vahedTaeidCode','vahedTasvibCode','vahedTaeidCode','typeMadrakCode','systemMortabetCode' , 'outdated' )
     resource_class  = MostanadatDakheliResource
     
     




@admin.register(MostanadatKhareji)
class MostanadatKharejiAdmin(ImportExportModelAdmin):
     list_display = ('title','kharejiSanadCode','processCode' ,'versionNumber','refrenceName','expiredDate' ,'postmasolUpdate','updatePeriod'  )
     list_filter = ('title','kharejiSanadCode','processCode' ,'versionNumber','refrenceName','expiredDate' ,'postmasolUpdate','updatePeriod'  )
     search_fields = ('title','kharejiSanadCode','processCode' ,'versionNumber','refrenceName','expiredDate' ,'postmasolUpdate','updatePeriod'  )
     resource_class  = MostanadatKharejiResource
     

@admin.register(TextDataBase)
class TextDataBaseAdmin(ImportExportModelAdmin):
     list_display = ('title',)
     list_filter = ('title',)
     search_fields = ('title',)
     resource_class  = TextDataBaseResource
     

@admin.register(BoolDataBase)
class BoolDataBaseAdmin(ImportExportModelAdmin):
     list_display = ('title',)
     list_filter = ('title',)
     search_fields = ('title',)
     resource_class  = BoolDataBaseResource
     

@admin.register(ConfirmationDataBase)
class ConfirmationDataBaseAdmin(ImportExportModelAdmin):
     list_display = ('title',)
     list_filter = ('title',)
     search_fields = ('title',)
     resource_class  = ConfirmationDataBaseResource
     

@admin.register(MostanadatDakheliChangeActivityManager)
class MostanadatDakheliChangeActivityManagerAdmin(ImportExportModelAdmin):
     list_display = ('status' ,'activity' ,'MostanadatDakheliChangeRelated')
     list_filter = ('status' ,'activity' ,'MostanadatDakheliChangeRelated')
     search_fields = ('status' ,'activity' ,'MostanadatDakheliChangeRelated')
     resource_class  = MostanadatDakheliChangeActivityManagerResource
     
@admin.register(MostanadatDakheliChange)
class MostanadatDakheliChangeAdmin(ImportExportModelAdmin):
     list_display = ('id',)
     list_filter = ('id',)
     search_fields = ('id',)
     resource_class  = MostanadatDakheliChangeResource
@admin.register(RecordDataBase)
class RecordDataBaseResourceChangeAdmin(ImportExportModelAdmin):
     list_display = ('id',)
     list_filter = ('id',)
     search_fields = ('id',)
     resource_class  = RecordDataBaseResource
@admin.register(RecordChange)
class RecordChangeResourceChangeAdmin(ImportExportModelAdmin):
     list_display = ('id',)
     list_filter = ('id',)
     search_fields = ('id',)
     resource_class  = RecordChangeResource
@admin.register(RecordChangeActivityManager)
class RecordChangeActivityManagerResourceChangeAdmin(ImportExportModelAdmin):
     list_display = ('id',)
     list_filter = ('id',)
     search_fields = ('id',)
     resource_class  = RecordChangeActivityManagerResource
     
     

