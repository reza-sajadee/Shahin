from django.contrib import admin
from .models import TextDataBase , BoolDataBase , ConfirmationDataBase , MeetingProfile , MeetingDate , MeetingMember ,Meeting , MeetingInvitation , MeetingAgenda , MeetingEnactment , Member  , MeetingDocument , MeetingPlan
from import_export.admin import ImportExportModelAdmin 
from .resources import  TextDataBaseResource ,BoolDataBaseResource  ,ConfirmationDataBaseResource , MeetingProfileResource , MeetingDateResource ,MeetingMemberResource, MeetingResource , MeetingInvitationResource , MeetingAgendaResource , MeetingEnactmentResource , MemberResource  , MeetingDocumentResource , MeetingPlanResource


@admin.register(MeetingProfile)
class MeetingProfileAdmin(ImportExportModelAdmin):
     list_display = ('id' ,)
     list_filter = ('id' ,)
     search_fields = ('id' ,)
     resource_class  = MeetingProfileResource
@admin.register(TextDataBase)
class TextDataBaseAdmin(ImportExportModelAdmin):
     list_display = ('title', )
     list_filter = ('title', )
     search_fields = ('title',)
     resource_class  = TextDataBaseResource
@admin.register(Meeting)
class MeetingAdmin(ImportExportModelAdmin):
     list_display = ('title', )
     list_filter = ('title', )
     search_fields = ('title',)
     resource_class  = MeetingResource
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
@admin.register(MeetingDate)
class MeetingDateAdmin(ImportExportModelAdmin):
     list_display = ('id', )
     list_filter = ('id', )
     search_fields = ('id',)
     resource_class  = MeetingDateResource
@admin.register(MeetingMember)
class MeetingMemberAdmin(ImportExportModelAdmin):
     list_display = ('id', )
     list_filter = ('id', )
     search_fields = ('id',)
     resource_class  = MeetingMemberResource
@admin.register(MeetingInvitation)
class MeetingInvitationAdmin(ImportExportModelAdmin):
     list_display = ('id', )
     list_filter = ('id', )
     search_fields = ('id',)
     resource_class  = MeetingInvitationResource
@admin.register(MeetingAgenda)
class MeetingAgendaAdmin(ImportExportModelAdmin):
     list_display = ('id', )
     list_filter = ('id', )
     search_fields = ('id',)
     resource_class  = MeetingAgendaResource
@admin.register(MeetingEnactment)
class MeetingEnactmentAdmin(ImportExportModelAdmin):
     list_display = ('id', )
     list_filter = ('id', )
     search_fields = ('id',)
     resource_class  = MeetingEnactmentResource
@admin.register(Member)
class MemberAdmin(ImportExportModelAdmin):
     list_display = ('id', )
     list_filter = ('id', )
     search_fields = ('id',)
     resource_class  = MemberResource
# @admin.register(MeetingMinute)
# class MeetingMinuteAdmin(ImportExportModelAdmin):
#      list_display = ('id', )
#      list_filter = ('id', )
#      search_fields = ('id',)
#      resource_class  = MeetingMinuteResource
@admin.register(MeetingDocument)
class MeetingDocumentAdmin(ImportExportModelAdmin):
     list_display = ('id', )
     list_filter = ('id', )
     search_fields = ('id',)
     resource_class  = MeetingDocumentResource
@admin.register(MeetingPlan)
class MeetingPlanAdmin(ImportExportModelAdmin):
     list_display = ('id', )
     list_filter = ('id', )
     search_fields = ('id',)
     resource_class  = MeetingPlanResource



# Register your models here.
