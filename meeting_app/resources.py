from import_export import resources
from .models import MeetingProfile , TextDataBase , BoolDataBase  , ConfirmationDataBase , MeetingDate , MeetingMember , Meeting , MeetingInvitation ,MeetingAgenda , MeetingEnactment , Member  , MeetingDocument,  MeetingDocument , MeetingPlan

class MeetingProfileResource(resources.ModelResource):
     class Meta:
          model = MeetingProfile
class MeetingResource(resources.ModelResource):
     class Meta:
          model = Meeting

class TextDataBaseResource(resources.ModelResource):
     class Meta:
          model = TextDataBase

class BoolDataBaseResource(resources.ModelResource):
     class Meta:
          model = BoolDataBase

class ConfirmationDataBaseResource(resources.ModelResource):
     class Meta:
          model = ConfirmationDataBase
class MeetingDateResource(resources.ModelResource):
     class Meta:
          model = MeetingDate
class MeetingMemberResource(resources.ModelResource):
     class Meta:
          model = MeetingMember
          
class MeetingInvitationResource(resources.ModelResource):
     class Meta:
          model = MeetingInvitation
class MeetingAgendaResource(resources.ModelResource):
     class Meta:
          model = MeetingAgenda
class MeetingEnactmentResource(resources.ModelResource):
     class Meta:
          model = MeetingEnactment
class MemberResource(resources.ModelResource):
     class Meta:
          model = Member
# class MeetingMinuteResource(resources.ModelResource):
#      class Meta:
#           model = MeetingMinute
class MeetingDocumentResource(resources.ModelResource):
     class Meta:
          model = MeetingDocument
class MeetingPlanResource(resources.ModelResource):
     class Meta:
          model = MeetingPlan
          
    