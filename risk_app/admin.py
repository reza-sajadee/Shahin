from django.contrib import admin
from .models import  QuestionDaste , RiskProfile  ,RiskTeam,RiskIdentification,RiskTopic , RiskActivityManager,RiskIdentificationSelecting , RiskMeasurement ,RiskProcessRelated , RiskProcess , extraData
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .resources import QuestionDasteResource  ,RiskProfileResource , RiskTeamResource, RiskIdentificationResource , RiskTopicResource , RiskActivityManagerResource ,RiskIdentificationSelectingResource , RiskMeasurementResource , RiskProcessRelatedResource , RiskProcessResource , extraDataResource
# Register your models here.standardTableResource


# Register your models here.
@admin.register(QuestionDaste)
class QuestionDasteAdmin(ImportExportModelAdmin):
     list_display = ('title' , )
     list_filter = ('title' , )
     search_fields = ('title' ,)
     resource_class  = QuestionDasteResource
     

     

@admin.register(RiskProfile)
class riskProfileAdmin(ImportExportModelAdmin):
     list_display = ('title' ,'committeeRisk' )
     list_filter = ('title' ,'committeeRisk' )
     search_fields = ('title' ,'committeeRisk' )
     resource_class  = RiskProfileResource
     
     

@admin.register(RiskTeam)
class riskProfileAdmin(ImportExportModelAdmin):
     list_display = ('title' ,'riskProfile' )
     list_filter = ('title' ,'riskProfile' )
     search_fields = ('title' ,'riskProfile' )
     resource_class  = RiskTeamResource
     

@admin.register(RiskIdentification)
class riskIdentificationAdmin(ImportExportModelAdmin):
     list_display = ('riskFailureModes','group','process'  ,'hoze' )
     list_filter = ('riskFailureModes','group','process'  ,'hoze' )
     search_fields = ('riskFailureModes','group','process'  ,'hoze' )
     resource_class  = RiskIdentificationResource
     
@admin.register(RiskIdentificationSelecting)
class RiskIdentificationSelectingAdmin(ImportExportModelAdmin):
    
     resource_class  = RiskIdentificationSelectingResource     

@admin.register(RiskTopic)
class RiskTopicAdmin(ImportExportModelAdmin):
     list_display = ('title' , )
     list_filter = ('title' , )
     search_fields = ('title' ,)
     resource_class  = RiskTopicResource
     

     
@admin.register(RiskActivityManager)
class RiskActivityManagerAdmin(ImportExportModelAdmin):
     list_display = ('sender' , 'reciver' , 'status','activity','team' )
     list_filter = ('sender' , 'reciver' , 'status','activity','team' )
     search_fields = ('sender' , 'reciver' , 'status','activity','team' )
     resource_class  = RiskActivityManagerResource
     
     



@admin.register(RiskMeasurement)
class RiskMeasurementAdmin(ImportExportModelAdmin):
     list_display = ('riskSeverity' , 'riskOccurrence' , 'riskDetection','riskIdentificated' )
     list_filter = ('riskSeverity' , 'riskOccurrence' , 'riskDetection','riskIdentificated' )
     search_fields = ('riskSeverity' , 'riskOccurrence' , 'riskDetection','riskIdentificated' )
     resource_class  = RiskMeasurementResource
     

@admin.register(RiskProcessRelated)
class RiskProcessRelatedAdmin(ImportExportModelAdmin):
     list_display = ('title' , )
     list_filter = ('title' , )
     search_fields = ('title' ,)
     resource_class  = RiskProcessRelatedResource


@admin.register(RiskProcess)
class RiskProcessAdmin(ImportExportModelAdmin):
     list_display = ('process' , )
     list_filter = ('process' , )
     search_fields = ('process' ,)
     resource_class  = RiskProcessResource
@admin.register(extraData)
class extraDataAdmin(ImportExportModelAdmin):
     list_display = ('id' , )
     list_filter = ('id' , )
     search_fields = ('id' ,)
     resource_class  = extraDataResource
     