from django.contrib import admin
from .models import TypeMomayezi , ReportMomayezi , ForsatBehbod ,NoghatGhovat ,AdamEntebagh ,CalenderMomayezi,RoleMomayezi , MomayeziTeam , MomayeziActivityManager , CheckListMomayezi , MomayeziTeamRequest , QuestionMomayeziList
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .resources import TypeMomayeziResource , ReportMomayeziResource , ForsatBehbodResource ,NoghatGhovatResource ,AdamEntebaghResource ,CalenderMomayeziResource,RoleMomayeziResource  , MomayeziTeamResource , MomayeziActivityManagerResource , CheckListMomayeziResource , MomayeziTeamRequestResource , QuestionMomayeziListResource






@admin.register(TypeMomayezi)
class TypeMomayeziAdmin(ImportExportModelAdmin):
     list_display = ('title','typeMomayeziCode' )
     list_filter = ('title','typeMomayeziCode' )
     search_fields = ('title','typeMomayeziCode')
     resource_class  = TypeMomayeziResource
     
     
@admin.register(ReportMomayezi)
class ReportMomayeziAdmin(ImportExportModelAdmin):
     list_display = ('report', )
     list_filter = ('report',  )
     search_fields = ('report',  )
     resource_class  = ReportMomayeziResource
     
     
@admin.register(ForsatBehbod)
class ForsatBehbodAdmin(ImportExportModelAdmin):
     list_display = ('title', 'created_at')
     list_filter = ('title', )
     search_fields = ('title',)
     resource_class  = ForsatBehbodResource
     
     
@admin.register(NoghatGhovat)
class NoghatGhovatAdmin(ImportExportModelAdmin):
     list_display = ('title', 'created_at' )
     list_filter = ('title', )
     search_fields = ('title',)
     resource_class  = NoghatGhovatResource
     
@admin.register(AdamEntebagh)
class AdamEntebaghAdmin(ImportExportModelAdmin):
     list_display = ('title', 'created_at' )
     list_filter = ('title', )
     search_fields = ('title',)
     resource_class  = AdamEntebaghResource
     
@admin.register(CalenderMomayezi)
class CalenderMomayeziAdmin(ImportExportModelAdmin):
     list_display = ('dateMomayezi','vahedMomayezi' ,'timeDuration','teamMomayezi' )
     list_filter = ('dateMomayezi','vahedMomayezi' ,'timeDuration','teamMomayezi' )
     search_fields = ('dateMomayezi','vahedMomayezi' ,'timeDuration','teamMomayezi' )
     resource_class  = CalenderMomayeziResource    


@admin.register(RoleMomayezi)
class RoleMomayeziAdmin(ImportExportModelAdmin):
     list_display = ('title', )
     list_filter = ('title', )
     search_fields = ('title',)
     resource_class  = RoleMomayeziResource
     
@admin.register(MomayeziTeam)
class MomayeziTeamAdmin(ImportExportModelAdmin):
     list_display = ('title', )
     list_filter = ('title', )
     search_fields = ('title',)
     resource_class  = MomayeziTeamResource


@admin.register(MomayeziTeamRequest)
class MomayeziTeamRequestAdmin(ImportExportModelAdmin):
     list_display = ('memberMomayezi', )
     list_filter = ('memberMomayezi', )
     search_fields = ('memberMomayezi',)
     resource_class  = MomayeziTeamRequestResource
     
@admin.register(MomayeziActivityManager)
class MomayeziActivityManagerAdmin(ImportExportModelAdmin):
     list_display = ('reciver','activity' ,'status' )
     list_filter = ('activity' ,'status')
     search_fields = ('reciver','activity')
     resource_class  = MomayeziActivityManagerResource
     
     
@admin.register(CheckListMomayezi)
class CheckListMomayeziAdmin(ImportExportModelAdmin):
     list_display = ('title', )
     list_filter = ('title', )
     search_fields = ('title',)
     resource_class  = CheckListMomayeziResource
@admin.register(QuestionMomayeziList)
class QuestionMomayeziListAdmin(ImportExportModelAdmin):
     list_display = ('question', 'vahedQuestion' )
     list_filter = ('question', 'vahedQuestion' )
     search_fields = ('question', 'vahedQuestion' )
     resource_class  = QuestionMomayeziListResource
     
     
     
     

