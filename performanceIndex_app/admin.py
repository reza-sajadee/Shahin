from django.contrib import admin
from .models import   TextDataBase , BoolDataBase,    ConfirmationDataBase ,SubjectPerformanceIndex ,TopicPerformanceIndex ,PerformanceIndex ,VariableDataBase ,PerformanceFormula ,PerformanceIndexActivityManager , PerformanceSettings
from import_export.admin import ImportExportModelAdmin
from .resources import    TextDataBaseResource ,BoolDataBaseResource     ,ConfirmationDataBaseResource  ,SubjectPerformanceIndexResource ,TopicPerformanceIndexResource ,PerformanceIndexResource ,VariableDataBaseResource ,PerformanceFormulaResource,PerformanceIndexActivityManagerResource  ,PerformanceSettingsResource


@admin.register(PerformanceSettings)
class PerformanceSettingsAdmin(ImportExportModelAdmin):
     list_display = ('id', )
     list_filter = ('id', )
     search_fields = ('id',)
     resource_class  = PerformanceSettingsResource
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
@admin.register(SubjectPerformanceIndex)
class SubjectPerformanceIndexAdmin(ImportExportModelAdmin):
     list_display = ( )
     list_filter = ( )
     search_fields = ()
     resource_class  = SubjectPerformanceIndexResource
@admin.register(TopicPerformanceIndex)
class TopicPerformanceIndexAdmin(ImportExportModelAdmin):
     list_display = ('title', )
     list_filter = ('title', )
     search_fields = ('title',)
     resource_class  = TopicPerformanceIndexResource
@admin.register(PerformanceIndex)
class PerformanceIndexAdmin(ImportExportModelAdmin , ):
     list_display = ( 'title' , )
     list_filter = ( 'title' , )
     search_fields = ('title' , )
     resource_class  = PerformanceIndexResource
@admin.register(VariableDataBase)
class VariableDataBaseAdmin(ImportExportModelAdmin):
     list_display = ('title', )
     list_filter = ( 'title',)
     search_fields = ('title',)
     resource_class  = VariableDataBaseResource
@admin.register(PerformanceFormula)
class PerformanceFormulaAdmin(ImportExportModelAdmin):
     list_display = ('acceptableCondition' , )
     list_filter = ( 'acceptableCondition' ,)
     search_fields = ('acceptableCondition' ,)
     resource_class  = PerformanceFormulaResource
@admin.register(PerformanceIndexActivityManager)
class PerformanceIndexActivityManagerAdmin(ImportExportModelAdmin):
     list_display = ('id' , 'variableRelated' , 'status' )
     list_filter = ( 'id' ,'variableRelated' , 'status' )
     search_fields = ('id' , 'variableRelated' , 'status')
     resource_class  = PerformanceIndexActivityManagerResource
 



# Register your models here.
